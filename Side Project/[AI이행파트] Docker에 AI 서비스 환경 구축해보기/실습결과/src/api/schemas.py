from pydantic import BaseModel, Field, validator
from typing import Optional, List

class PredictRequest(BaseModel):
    """Request schema for sentiment prediction"""
    text: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description="Text to analyze for sentiment",
        example="I love this product! It's amazing."
    )

    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()

class PredictResponse(BaseModel):
    """Response schema for sentiment prediction"""
    sentiment: str = Field(
        ...,
        description="Predicted sentiment",
        example="positive"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1",
        example=0.95
    )
    processing_time: float = Field(
        ...,
        ge=0.0,
        description="Processing time in seconds",
        example=0.12
    )

class HealthResponse(BaseModel):
    """Response schema for health check"""
    status: str = Field(
        ...,
        description="Service status",
        example="healthy"
    )
    timestamp: str = Field(
        ...,
        description="Current timestamp",
        example="2025-09-27T14:30:00Z"
    )
    version: str = Field(
        ...,
        description="API version",
        example="1.0.0"
    )
    model_loaded: bool = Field(
        ...,
        description="Whether the AI model is loaded",
        example=True
    )

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str = Field(
        ...,
        description="Error description",
        example="Model not loaded"
    )

class BatchPredictRequest(BaseModel):
    """Request schema for batch sentiment prediction"""
    texts: List[str] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="List of texts to analyze for sentiment",
        example=["I love this!", "This is terrible", "It's okay"]
    )

    @validator('texts')
    def validate_texts(cls, v):
        if not v:
            raise ValueError('Texts list cannot be empty')
        # Validate each text
        validated = []
        for text in v:
            if not text or not text.strip():
                continue  # Skip empty texts
            if len(text) > 512:
                raise ValueError(f'Text too long (max 512 characters): {text[:50]}...')
            validated.append(text.strip())
        if not validated:
            raise ValueError('No valid texts provided')
        return validated

class BatchPredictResponse(BaseModel):
    """Response schema for batch sentiment prediction"""
    results: List[PredictResponse] = Field(
        ...,
        description="List of prediction results"
    )
    total_processed: int = Field(
        ...,
        description="Total number of texts processed",
        example=3
    )
    total_time: float = Field(
        ...,
        ge=0.0,
        description="Total processing time in seconds",
        example=0.35
    )