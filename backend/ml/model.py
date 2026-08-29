"""The autoencoder architecture, shared between training (ml/train_autoencoder.py)
and inference (app/vision/anomaly_model.py) so the two never drift apart.

Trained on clean images only. The encoder squeezes a 128x128 image down to an
8x8x256 bottleneck; the decoder tries to rebuild the original from that
bottleneck. Because it never saw defective images during training, it
reconstructs them poorly — that reconstruction error is the anomaly signal.
"""

import torch.nn as nn

IMAGE_SIZE = 128


class ConvAutoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),    # 128 -> 64
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),   # 64 -> 32
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),  # 32 -> 16
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1), # 16 -> 8
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1), # 8 -> 16
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),  # 16 -> 32
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1),   # 32 -> 64
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, kernel_size=4, stride=2, padding=1),    # 64 -> 128
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))
