"""
Pydantic request/response schemas for PhishGuard API.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime


# ── Request ────────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def url_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL must not be empty")
        if len(v) > 2048:
            raise ValueError("URL is too long (max 2048 characters)")
        return v


# ── Responses ──────────────────────────────────────────────────────────────

class PredictResponse(BaseModel):
    scan_id: str
    url: str
    prediction: str          # "SAFE" | "PHISHING"
    confidence: float        # 0.0 – 1.0  (probability of predicted class)
    phishing_probability: float
    safe_probability: float
    features: Dict[str, float]
    timestamp: datetime


class ScanRecord(BaseModel):
    id: str
    url: str
    prediction: str
    confidence: float
    phishing_probability: float
    features: Dict[str, float]
    created_at: datetime


class HistoryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    records: List[ScanRecord]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: Optional[str] = None
    accuracy: Optional[float] = None
    feature_count: Optional[int] = None
    database_connected: bool


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
