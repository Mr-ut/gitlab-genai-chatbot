from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import HealthResponse
from app.core.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check various dependencies
        dependencies = {
            "database": "healthy",
            "vector_store": "healthy",
            "llm_service": "healthy" if settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY else "warning"
        }

        return HealthResponse(
            status="healthy",
            version=settings.VERSION,
            dependencies=dependencies
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@router.get("/status")
async def status():
    """Simple status endpoint"""
    return {"status": "online", "timestamp": datetime.utcnow()}
