"""Trains the anomaly-detection autoencoder on MVTec AD 'bottle' (clean
images only), evaluates it against the labeled test set, and saves the
weights + calibrated threshold that app/vision/anomaly_model.py loads at
inference time.

Mirrors the training run actually used for the shipped model (see
ml/artifacts/metadata.json for those results) — re-running this will
reproduce similar, not necessarily identical, numbers, since training is
stochastic.

Usage (from backend/, after running ml/download_dataset.py):
    python -m ml.train_autoencoder
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
from sklearn.metrics import roc_auc_score, roc_curve
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from ml.model import IMAGE_SIZE, ConvAutoencoder

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "mvtec" / "bottle"
ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
EPOCHS = 50
BATCH_SIZE = 16
LEARNING_RATE = 1e-3

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
])


class GoodImagesDataset(Dataset):
    """Only clean/defect-free images — what the autoencoder learns from."""

    def __init__(self, folder: Path):
        self.paths = [folder / f for f in os.listdir(folder)]

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        image = Image.open(self.paths[idx]).convert("RGB")
        return transform(image)


class LabeledTestDataset(Dataset):
    """Every test image, tagged with its true label (0 = good, 1 = defective)."""

    def __init__(self, test_dir: Path):
        self.samples = []
        for folder in os.listdir(test_dir):
            label = 0 if folder == "good" else 1
            for fname in os.listdir(test_dir / folder):
                self.samples.append((test_dir / folder / fname, label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        return transform(image), label


def per_image_error(model: ConvAutoencoder, images: torch.Tensor, device: torch.device) -> np.ndarray:
    """Reconstruction MSE for each image in the batch, kept separate (not averaged)."""
    images = images.to(device)
    with torch.no_grad():
        reconstructed = model(images)
    return ((reconstructed - images) ** 2).mean(dim=[1, 2, 3]).cpu().numpy()


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    train_dataset = GoodImagesDataset(DATA_DIR / "train" / "good")
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    print("Training images:", len(train_dataset))

    model = ConvAutoencoder().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        for images in train_loader:
            images = images.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, images)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / len(train_dataset)
        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"Epoch {epoch + 1}/{EPOCHS} - reconstruction loss: {epoch_loss:.5f}")

    # Calibrate the anomaly threshold from clean training data only — we
    # deliberately don't look at the labeled test set here, since in
    # production we won't have ground-truth labels for new images either.
    model.eval()
    train_errors = np.concatenate([per_image_error(model, images, device) for images in train_loader])
    print(f"Train error - mean: {train_errors.mean():.6f}, std: {train_errors.std():.6f}")

    test_dataset = LabeledTestDataset(DATA_DIR / "test")
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    test_errors, test_labels = [], []
    for images, labels in test_loader:
        test_errors.extend(per_image_error(model, images, device))
        test_labels.extend(labels.numpy())
    test_errors = np.array(test_errors)
    test_labels = np.array(test_labels)

    auc = roc_auc_score(test_labels, test_errors)
    fpr, tpr, thresholds = roc_curve(test_labels, test_errors)
    best_idx = (tpr - fpr).argmax()  # Youden's J statistic: best true/false-positive tradeoff
    threshold = float(thresholds[best_idx])

    print(f"ROC-AUC: {auc:.4f}")
    print(f"Chosen threshold (Youden's J): {threshold:.7f}")
    print(f"  -> recall on defective: {tpr[best_idx]:.2%}, false-positive rate on good: {fpr[best_idx]:.2%}")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), ARTIFACTS_DIR / "autoencoder.pth")

    metadata = {
        "architecture": "ConvAutoencoder (see ml/model.py)",
        "image_size": IMAGE_SIZE,
        "trained_on": f"MVTec AD - bottle category, train/good split ({len(train_dataset)} images)",
        "epochs": EPOCHS,
        "evaluation": {
            "test_set": f"MVTec AD bottle test split ({len(test_dataset)} images)",
            "roc_auc": float(auc),
            "threshold": threshold,
            "threshold_method": "Youden's J statistic on ROC curve",
            "recall_defective": float(tpr[best_idx]),
            "false_positive_rate_good": float(fpr[best_idx]),
        },
    }
    (ARTIFACTS_DIR / "metadata.json").write_text(json.dumps(metadata, indent=2))
    print("Saved model + metadata to", ARTIFACTS_DIR)


if __name__ == "__main__":
    main()
