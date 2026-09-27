"""
Scan history routes:
  GET    /api/history           — paginated list
  GET    /api/history/{scan_id} — single record
  DELETE /api/history           — clear all
"""
import logging
from fastapi import APIRouter, HTTPException, Query, status

from app.models.schemas import HistoryResponse, ScanRecord
from app.services import database as db_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/history", response_model=HistoryResponse, tags=["History"])
async def get_history(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Records per page"),
) -> HistoryResponse:
    data = await db_service.get_scans(page=page, page_size=page_size)
    records = [ScanRecord(**r) for r in data["records"]]
    return HistoryResponse(
        total=data["total"],
        page=data["page"],
        page_size=data["page_size"],
        records=records,
    )


@router.get("/history/{scan_id}", response_model=ScanRecord, tags=["History"])
async def get_scan(scan_id: str) -> ScanRecord:
    doc = await db_service.get_scan_by_id(scan_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan with id '{scan_id}' not found.",
        )
    return ScanRecord(**doc)


@router.delete("/history", tags=["History"])
async def clear_history() -> dict:
    deleted = await db_service.delete_all_scans()
    return {"message": f"Deleted {deleted} scan records.", "deleted": deleted}
