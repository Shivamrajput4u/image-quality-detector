"""Rule-based quality scoring from classical CV statistics.

Thresholds below are starting points calibrated by eye for natural photos
normalized to a 600px-wide grayscale frame (see classical.py). They're meant
to be revisited once real evaluation images are run through the pipeline —
see the README's evaluation section.

anomaly_score comes from the trained autoencoder (see anomaly_model.py) —
a reconstruction-error signal that flags structural defects the stats above
can't see. ANOMALY_THRESHOLD was calibrated via Youden's J statistic on the
MVTec AD bottle test set (see ml/artifacts/metadata.json). If no trained
model is present, both come back None and this function falls back to the
classical stats alone.
"""

from __future__ import annotations

from app.vision.anomaly_model import ANOMALY_THRESHOLD


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _confidence(distance_ratio: float) -> float:
    """Map 'how far past the threshold' (0-1ish) to a 0.5-0.95 confidence score."""
    return round(_clamp(0.5 + distance_ratio * 0.45, 0.5, 0.95), 2)


def score_issues(stats: dict, anomaly_score: float | None = None) -> tuple[int, str, list[dict]]:
    """Combine classical CV stats (and, once trained, the anomaly score) into
    an overall quality score (0-100), a label, and a list of detected issues."""
    issues: list[dict] = []
    score = 100

    sharpness = stats["sharpness"]
    if sharpness < 250:
        if sharpness < 30:
            severity, penalty = "high", 40
        elif sharpness < 100:
            severity, penalty = "medium", 22
        else:
            severity, penalty = "low", 10
        issues.append({"type": "blur", "severity": severity, "confidence": _confidence((250 - sharpness) / 250)})
        score -= penalty

    brightness = stats["brightness"]
    if brightness < 80:
        if brightness < 35:
            severity, penalty = "high", 35
        elif brightness < 60:
            severity, penalty = "medium", 18
        else:
            severity, penalty = "low", 8
        issues.append({
            "type": "underexposure", "severity": severity, "confidence": _confidence((80 - brightness) / 80),
        })
        score -= penalty
    elif brightness > 190:
        if brightness > 235:
            severity, penalty = "high", 35
        elif brightness > 215:
            severity, penalty = "medium", 18
        else:
            severity, penalty = "low", 8
        issues.append({
            "type": "overexposure", "severity": severity, "confidence": _confidence((brightness - 190) / 65),
        })
        score -= penalty

    noise = stats["noise"]
    if noise > 3:
        if noise > 10:
            severity, penalty = "high", 30
        elif noise > 6:
            severity, penalty = "medium", 16
        else:
            severity, penalty = "low", 7
        issues.append({"type": "noise", "severity": severity, "confidence": _confidence((noise - 3) / 10)})
        score -= penalty

    contrast = stats["contrast"]
    if contrast < 25:
        severity, penalty = ("high", 15) if contrast < 12 else ("low", 6)
        issues.append({
            "type": "low_contrast", "severity": severity, "confidence": _confidence((25 - contrast) / 25),
        })
        score -= penalty

    if anomaly_score is not None and ANOMALY_THRESHOLD is not None and anomaly_score > ANOMALY_THRESHOLD:
        severity = "high" if anomaly_score > ANOMALY_THRESHOLD * 2 else "medium"
        issues.append({
            "type": "potential_defect",
            "severity": severity,
            "confidence": _confidence(min(1.0, anomaly_score / (ANOMALY_THRESHOLD * 2))),
        })
        score -= 30 if severity == "high" else 15

    score = round(_clamp(score, 0, 100))
    if score >= 75:
        label = "ACCEPTABLE"
    elif score >= 40:
        label = "DEGRADED"
    else:
        label = "DEFECTIVE"

    return score, label, issues
