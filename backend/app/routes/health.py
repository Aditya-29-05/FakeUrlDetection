"""
GET /api/health  — liveness + readiness check.
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services import predictor as pred_service
from app.services import database as db_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    model_loaded = pred_service.predictor.is_loaded
    metadata = pred_service.predictor.metadata

    metrics = metadata.get("metrics", {})
    accuracy = metrics.get("accuracy")
    model_version = metadata.get("model_version")
    feature_count = metadata.get("feature_count")

    return HealthResponse(
        status="ok" if model_loaded else "degraded",
        model_loaded=model_loaded,
        model_version=model_version,
        accuracy=accuracy,
        feature_count=feature_count,
        database_connected=db_service.is_connected(),
    )
