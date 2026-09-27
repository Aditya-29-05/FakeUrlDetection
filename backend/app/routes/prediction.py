"""
POST /api/predict  — URL phishing prediction endpoint.
"""
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status

from app.models.schemas import PredictRequest, PredictResponse
from app.services import predictor as pred_service
from app.services import database as db_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predict", response_model=PredictResponse, tags=["Prediction"])
async def predict_url(request: PredictRequest) -> PredictResponse:
    if not pred_service.predictor.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Check server logs.",
        )

    try:
        prediction_label, confidence, phishing_prob, safe_prob, features = pred_service.predictor.predict(request.url)
    except Exception as exc:
        logger.exception("Prediction failed for url=%r", request.url)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(exc)}",
        )

    # Persist to MongoDB (non-blocking; failure doesn't break response)
    scan_id = ""
    try:
        scan_id = await db_service.insert_scan(
            url=request.url,
            prediction=prediction_label,
            confidence=confidence,
            phishing_probability=phishing_prob,
            features=features,
        )
    except Exception as exc:
        logger.warning("Failed to save scan to MongoDB: %s", exc)

    return PredictResponse(
        scan_id=scan_id,
        url=request.url,
        prediction=prediction_label,
        confidence=confidence,
        phishing_probability=phishing_prob,
        safe_probability=safe_prob,
        features=features,
        timestamp=datetime.now(timezone.utc),
    )
