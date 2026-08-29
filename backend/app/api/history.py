from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.analysis import AnalysisResult
from app.schemas.analysis import AnalysisListResponse, AnalysisResponse

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/analyses", response_model=AnalysisListResponse)
def list_analyses(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)) -> AnalysisListResponse:
    query = db.query(AnalysisResult).order_by(desc(AnalysisResult.created_at))
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    return AnalysisListResponse(total=total, results=[AnalysisResponse.from_result(r) for r in results])


@router.get("/analyses/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)) -> AnalysisResponse:
    result = db.get(AnalysisResult, analysis_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return AnalysisResponse.from_result(result)
