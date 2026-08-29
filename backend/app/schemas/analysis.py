from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Issue(BaseModel):
    type: str
    severity: str
    confidence: float


class AnalysisResponse(BaseModel):
    id: int
    original_filename: str
    image_url: str
    quality_score: int
    quality_label: str
    issues: list[Issue]
    stats: dict
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_result(cls, result) -> "AnalysisResponse":
        """Build the API response from an AnalysisResult row, adding the
        servable image_url (derived from stored_path, not a DB column)."""
        return cls(
            id=result.id,
            original_filename=result.original_filename,
            image_url=f"/uploads/{result.stored_path}",
            quality_score=result.quality_score,
            quality_label=result.quality_label,
            issues=result.issues,
            stats=result.stats,
            created_at=result.created_at,
        )


class AnalysisListResponse(BaseModel):
    total: int
    results: list[AnalysisResponse]
