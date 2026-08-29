from __future__ import annotations

import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.analysis import AnalysisResult
from app.vision.anomaly_model import get_anomaly_score
from app.vision.classical import compute_stats, decode_image
from app.vision.scoring import score_issues


def analyze_and_store(db: Session, filename: str, file_bytes: bytes) -> AnalysisResult:
    """Decode the image, run quality analysis, persist both the file and the
    result row, and return the saved AnalysisResult.

    Raises InvalidImageError (from vision.classical) for unreadable/corrupt
    bytes — the API layer turns that into a 400 response.
    """
    image = decode_image(file_bytes)
    stats = compute_stats(image)
    anomaly_score = get_anomaly_score(image)
    score, label, issues = score_issues(stats, anomaly_score)

    stored_name = f"{uuid.uuid4().hex}{Path(filename).suffix.lower() or '.jpg'}"
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / stored_name).write_bytes(file_bytes)

    result = AnalysisResult(
        original_filename=filename,
        stored_path=stored_name,
        quality_score=score,
        quality_label=label,
        issues=issues,
        stats=stats,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
