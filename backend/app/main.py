"""
PhishGuard FastAPI application factory.
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.services import predictor as pred_service
from app.services import database as db_service
from app.routes import health, prediction, history

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    settings = get_settings()

    # Resolve model path relative to this file's parent (backend/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, settings.model_path)
    metadata_path = os.path.join(base_dir, settings.metadata_path)

    # Load ML model
    try:
        pred_service.predictor.load(model_path, metadata_path)
    except FileNotFoundError as exc:
        logger.error("CRITICAL — model file missing: %s", exc)

    # Connect to MongoDB
    await db_service.connect(settings.mongodb_uri, settings.database_name)

    logger.info("PhishGuard API ready on http://%s:%s", settings.host, settings.port)
    yield

    # Shutdown
    await db_service.disconnect()
    logger.info("PhishGuard API shutdown complete.")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="PhishGuard API",
        description="Phishing URL detection API powered by XGBoost.",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # CORS — only allow configured origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Routers
    prefix = "/api"
    app.include_router(health.router,     prefix=prefix)
    app.include_router(prediction.router, prefix=prefix)
    app.include_router(history.router,    prefix=prefix)

    @app.get("/", include_in_schema=False)
    async def root():
        return {"service": "PhishGuard API", "docs": "/api/docs"}

    return app


app = create_app()
