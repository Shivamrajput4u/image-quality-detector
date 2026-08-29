"""Learned anomaly-detection component (PyTorch autoencoder).

Not wired in yet. This is the seam Step 3 fills in: once you've trained
ml/train_autoencoder.py and dropped the resulting weights at
ml/artifacts/autoencoder.pth, get_anomaly_score() starts returning a real
reconstruction-error score instead of None, and scoring.py automatically
starts using it (see the anomaly_score parameter there).

Until then, the rule-based classical stats alone drive the result.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

_MODEL_PATH = Path(__file__).resolve().parents[2] / "ml" / "artifacts" / "autoencoder.pth"


def get_anomaly_score(image: np.ndarray) -> float | None:
    """Return a reconstruction-error anomaly score for the image, or None if
    no trained model is available yet."""
    if not _MODEL_PATH.exists():
        return None
    raise NotImplementedError(
        "autoencoder.pth found but inference isn't wired up yet — that's Step 3."
    )
