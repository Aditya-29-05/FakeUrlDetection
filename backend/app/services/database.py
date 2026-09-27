"""
Async MongoDB client using Motor.
Provides collection handles and helper CRUD operations for scan history.
"""
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

logger = logging.getLogger(__name__)

# Module-level client (set during startup)
_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None
_connected = False


async def connect(uri: str, database_name: str) -> None:
    """Open the Motor connection and ping the server."""
    global _client, _db, _connected
    try:
        _client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
        _db = _client[database_name]
        # Verify connection
        await _client.admin.command("ping")
        # Ensure index on createdAt for efficient pagination
        await _db["scan_history"].create_index([("createdAt", -1)])
        _connected = True
        logger.info("MongoDB connected: database=%s", database_name)
    except Exception as exc:
        _connected = False
        logger.warning("MongoDB connection failed: %s — history will be disabled.", exc)


async def disconnect() -> None:
    global _client, _connected
    if _client is not None:
        _client.close()
        _connected = False
        logger.info("MongoDB disconnected.")


def is_connected() -> bool:
    return _connected


def _collection() -> AsyncIOMotorCollection:
    if _db is None:
        raise RuntimeError("Database not initialised. Call connect() first.")
    return _db["scan_history"]


async def insert_scan(
    url: str,
    prediction: str,
    confidence: float,
    phishing_probability: float,
    features: Dict[str, float],
) -> str:
    """Insert a scan record and return its string id."""
    if not _connected:
        return ""
    doc = {
        "url": url,
        "prediction": prediction,
        "confidence": confidence,
        "phishing_probability": phishing_probability,
        "features": features,
        "createdAt": datetime.now(timezone.utc),
    }
    result = await _collection().insert_one(doc)
    return str(result.inserted_id)


async def get_scans(page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """Return a paginated list of scan records sorted newest first."""
    if not _connected:
        return {"total": 0, "page": page, "page_size": page_size, "records": []}

    col = _collection()
    total = await col.count_documents({})
    skip = (page - 1) * page_size
    cursor = col.find({}).sort("createdAt", -1).skip(skip).limit(page_size)

    records = []
    async for doc in cursor:
        records.append({
            "id": str(doc["_id"]),
            "url": doc.get("url", ""),
            "prediction": doc.get("prediction", ""),
            "confidence": doc.get("confidence", 0.0),
            "phishing_probability": doc.get("phishing_probability", 0.0),
            "features": doc.get("features", {}),
            "created_at": doc.get("createdAt", datetime.now(timezone.utc)),
        })

    return {"total": total, "page": page, "page_size": page_size, "records": records}


async def get_scan_by_id(scan_id: str) -> Optional[Dict[str, Any]]:
    """Return a single scan record by its ObjectId string."""
    if not _connected:
        return None
    try:
        oid = ObjectId(scan_id)
    except Exception:
        return None
    doc = await _collection().find_one({"_id": oid})
    if doc is None:
        return None
    return {
        "id": str(doc["_id"]),
        "url": doc.get("url", ""),
        "prediction": doc.get("prediction", ""),
        "confidence": doc.get("confidence", 0.0),
        "phishing_probability": doc.get("phishing_probability", 0.0),
        "features": doc.get("features", {}),
        "created_at": doc.get("createdAt", datetime.now(timezone.utc)),
    }


async def delete_all_scans() -> int:
    """Delete all scan history. Returns count of deleted documents."""
    if not _connected:
        return 0
    result = await _collection().delete_many({})
    return result.deleted_count
