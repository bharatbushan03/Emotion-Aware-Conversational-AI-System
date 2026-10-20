import logging
import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import endpoints
from app.core.config import settings
from app.services.emotion import emotion_service
from app.services.strategy import response_strategy

logger = logging.getLogger("app")


def _warmup_models() -> None:
    logger.info("Loading emotion and generation models")
    try:
        emotion_service.load_model()
        response_strategy.load_generator()
        logger.info("Models are ready")
    except Exception:
        logger.exception("Model warmup failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("SKIP_MODEL_WARMUP") != "1":
        threading.Thread(target=_warmup_models, name="model-warmup", daemon=True).start()
    yield


def _cors_origins() -> list[str]:
    return [
        origin.strip().rstrip("/")
        for origin in settings.ALLOWED_ORIGINS.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Emotion-Aware Conversational AI",
    description="Backend API for Emotion-Aware Conversational AI System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_origin_regex=settings.CORS_ORIGIN_REGEX or None,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Emotion-Aware AI Backend is running"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_ready": emotion_service.is_ready and response_strategy.is_ready,
        "version": "1.0.0",
    }
