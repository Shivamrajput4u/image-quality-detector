from __future__ import annotations

import cv2
import numpy as np


class InvalidImageError(ValueError):
    """Raised when uploaded bytes can't be decoded as an image (corrupt/unsupported)."""


def decode_image(data: bytes) -> np.ndarray:
    """Decode raw file bytes into a BGR OpenCV image, or raise InvalidImageError."""
    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None or image.size == 0:
        raise InvalidImageError("File is not a readable image (unsupported format or corrupted data).")
    return image


def _normalize_for_analysis(image: np.ndarray, target_width: int = 600) -> np.ndarray:
    """Resize to a fixed width so sharpness/noise measurements are comparable
    across images regardless of original resolution."""
    height, width = image.shape[:2]
    if width == target_width:
        return image
    scale = target_width / width
    return cv2.resize(image, (target_width, max(1, int(height * scale))), interpolation=cv2.INTER_AREA)


def _estimate_noise(gray: np.ndarray) -> float:
    """Fast noise-sigma estimate (Immerkaer, 1996). Convolving with this
    kernel cancels out smooth image structure, leaving mostly sensor noise,
    so its magnitude approximates the noise standard deviation."""
    kernel = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], dtype=np.float32)
    height, width = gray.shape
    convolved = cv2.filter2D(gray.astype(np.float32), -1, kernel)
    sigma = np.sum(np.abs(convolved)) * np.sqrt(0.5 * np.pi) / (6 * (width - 2) * (height - 2))
    return float(sigma)


def compute_stats(image: np.ndarray) -> dict:
    """Derive the raw image-quality measurements that scoring.py reasons over."""
    original_height, original_width = image.shape[:2]
    normalized = _normalize_for_analysis(image)
    gray = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(normalized, cv2.COLOR_BGR2HSV)

    return {
        "width": original_width,
        "height": original_height,
        # Variance of the Laplacian: low = flat/blurry, high = lots of sharp edges.
        "sharpness": round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2),
        # Mean pixel intensity, 0-255: low = underexposed, high = overexposed.
        "brightness": round(float(gray.mean()), 2),
        # Std of pixel intensity: low = flat/washed-out image.
        "contrast": round(float(gray.std()), 2),
        "noise": round(_estimate_noise(gray), 2),
        "saturation": round(float(hsv[:, :, 1].mean()), 2),
    }
