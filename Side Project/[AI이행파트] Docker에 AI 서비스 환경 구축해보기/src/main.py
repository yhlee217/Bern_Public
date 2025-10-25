from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime
import logging
from contextlib import asynccontextmanager

from api.endpoints import router
from models.sentiment_model import SentimentModel
from utils.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance
model_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_instance
    logger.info("Loading AI model...")
    try:
        model_instance = SentimentModel()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

    yield

    logger.info("Shutting down...")

# Get configuration
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global model_instance

    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.api_version,
        "model_loaded": model_instance is not None
    }

    if model_instance is None:
        status["status"] = "unhealthy"
        return JSONResponse(status_code=503, content=status)

    return status

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Sentiment Analysis Service",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }

def get_model():
    """Get the global model instance"""
    global model_instance
    if model_instance is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return model_instance

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug_mode,
        log_level=settings.log_level.lower()
    )