"""Learned anomaly-detection component (PyTorch autoencoder).

Loads the weights trained in ml/train_autoencoder.py (see
ml/artifacts/metadata.json for what it was trained on and how the
threshold was picked). If no trained model is present yet,
get_anomaly_score() returns None and scoring.py falls back to the
classical rule-based stats alone.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
import torch

from ml.model import IMAGE_SIZE, ConvAutoencoder

_ARTIFACTS_DIR = Path(__file__).resolve().parents[2] / "ml" / "artifacts"
_MODEL_PATH = _ARTIFACTS_DIR / "autoencoder.pth"
_METADATA_PATH = _ARTIFACTS_DIR / "metadata.json"

_model: ConvAutoencoder | None = None
ANOMALY_THRESHOLD: float | None = None

if _METADATA_PATH.exists():
    ANOMALY_THRESHOLD = json.loads(_METADATA_PATH.read_text())["evaluation"]["threshold"]


def _load_model() -> ConvAutoencoder | None:
    global _model
    if _model is not None:
        return _model
    if not _MODEL_PATH.exists():
        return None

    model = ConvAutoencoder()
    model.load_state_dict(torch.load(_MODEL_PATH, map_location="cpu"))
    model.eval()
    _model = model
    return _model


def get_anomaly_score(image: np.ndarray) -> float | None:
    """Return a reconstruction-error anomaly score for a BGR OpenCV image, or
    None if no trained model is available yet. Higher = more anomalous."""
    model = _load_model()
    if model is None:
        return None

    resized = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    tensor = torch.from_numpy(rgb).float().permute(2, 0, 1).unsqueeze(0) / 255.0

    with torch.no_grad():
        reconstruction = model(tensor)
        error = torch.mean((reconstruction - tensor) ** 2)

    return float(error.item())
