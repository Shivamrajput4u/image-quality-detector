from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AnalysisResult(Base):
    """One row per image that was uploaded and analyzed."""

    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    stored_path: Mapped[str] = mapped_column(String, nullable=False)

    quality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    quality_label: Mapped[str] = mapped_column(String, nullable=False)

    # List of {"type": "blur", "severity": "high", "confidence": 0.82}
    issues: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    # Raw measurements the score was derived from (sharpness, brightness, etc.)
    stats: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
