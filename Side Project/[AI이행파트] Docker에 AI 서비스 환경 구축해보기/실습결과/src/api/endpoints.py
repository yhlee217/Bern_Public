from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from typing import Any

from api.schemas import PredictRequest, PredictResponse, ErrorResponse, BatchPredictRequest, BatchPredictResponse
# from models.sentiment_model import SentimentModel  # 기존 영어 전용 모델
from models.sentiment_model_improved import SentimentModelImproved as SentimentModel  # 개선된 다국어 모델

logger = logging.getLogger(__name__)

router = APIRouter()

# Global model instance (will be set by main.py)
_model_instance = None

def get_model() -> SentimentModel:
    """Dependency to get the model instance"""
    global _model_instance
    if _model_instance is None:
        # Import here to avoid circular imports
        from main import get_model as main_get_model
        _model_instance = main_get_model()
    return _model_instance

@router.post(
    "/predict",
    response_model=PredictResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Predict text sentiment",
    description="Analyze the sentiment of the provided text and return the prediction with confidence score."
)
async def predict_sentiment(
    request: PredictRequest,
    model: SentimentModel = Depends(get_model)
) -> PredictResponse:
    """
    Predict sentiment for the given text.

    Returns:
    - sentiment: positive, negative, or neutral
    - confidence: confidence score between 0 and 1
    - processing_time: time taken for prediction in seconds
    """
    try:
        logger.info(f"Processing sentiment prediction for text length: {len(request.text)}")

        # Get prediction from model
        result = model.predict(request.text)

        logger.info(f"Prediction completed: {result['sentiment']} (confidence: {result['confidence']:.3f})")

        return PredictResponse(**result)

    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

@router.get(
    "/model/info",
    summary="Get model information",
    description="Get information about the loaded AI model."
)
async def get_model_info(model: SentimentModel = Depends(get_model)) -> dict[str, Any]:
    """Get information about the current model"""
    try:
        return model.get_model_info()
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model information")

@router.post(
    "/model/health",
    summary="Check model health",
    description="Perform a health check on the AI model by running a test prediction."
)
async def check_model_health(model: SentimentModel = Depends(get_model)) -> dict[str, Any]:
    """Check if the model is working correctly"""
    try:
        is_healthy = model.health_check()
        return {
            "model_healthy": is_healthy,
            "status": "healthy" if is_healthy else "unhealthy"
        }
    except Exception as e:
        logger.error(f"Model health check failed: {e}")
        return {
            "model_healthy": False,
            "status": "unhealthy",
            "error": str(e)
        }

@router.post(
    "/predict/batch",
    response_model=BatchPredictResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Batch predict text sentiment",
    description="Analyze the sentiment of multiple texts in a single request for better performance."
)
async def batch_predict_sentiment(
    request: BatchPredictRequest,
    model: SentimentModel = Depends(get_model)
) -> BatchPredictResponse:
    """
    Predict sentiment for multiple texts in batch.

    This endpoint is optimized for processing multiple texts efficiently.
    Maximum 100 texts per request.

    Returns:
    - results: List of prediction results
    - total_processed: Number of texts processed
    - total_time: Total processing time
    """
    import time

    try:
        start_time = time.time()
        logger.info(f"Processing batch sentiment prediction for {len(request.texts)} texts")

        results = []
        for text in request.texts:
            try:
                result = model.predict(text)
                results.append(PredictResponse(**result))
            except Exception as e:
                logger.warning(f"Failed to predict for text: {text[:50]}... Error: {e}")
                # Add a default result for failed predictions
                results.append(PredictResponse(
                    sentiment="unknown",
                    confidence=0.0,
                    processing_time=0.0
                ))

        total_time = time.time() - start_time

        logger.info(f"Batch prediction completed: {len(results)} texts in {total_time:.3f}s")

        return BatchPredictResponse(
            results=results,
            total_processed=len(results),
            total_time=total_time
        )

    except ValueError as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Batch prediction failed")