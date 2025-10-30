#!/usr/bin/env python3
"""
간단한 감정분석 서비스 데모
실제 AI 모델 대신 규칙 기반 감정분석을 사용하여 API 구조를 테스트합니다.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
import time
import re
from datetime import datetime

# 간단한 감정분석 규칙
POSITIVE_WORDS = [
    "좋다", "훌륭", "멋져", "최고", "완벽", "사랑", "행복", "기쁘", "만족",
    "amazing", "great", "awesome", "perfect", "love", "happy", "excellent", "good"
]

NEGATIVE_WORDS = [
    "나쁘", "별로", "싫어", "최악", "실망", "화가", "짜증", "슬프", "무서",
    "terrible", "bad", "awful", "worst", "hate", "angry", "sad", "disappointed"
]

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=512)

class PredictResponse(BaseModel):
    sentiment: str
    confidence: float
    processing_time: float

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    model_loaded: bool

def analyze_sentiment_simple(text: str) -> dict:
    """간단한 규칙 기반 감정분석"""
    start_time = time.time()

    text_lower = text.lower()
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)

    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.9, 0.6 + (positive_count - negative_count) * 0.1)
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.9, 0.6 + (negative_count - positive_count) * 0.1)
    else:
        sentiment = "neutral"
        confidence = 0.7

    processing_time = time.time() - start_time

    return {
        "sentiment": sentiment,
        "confidence": round(confidence, 3),
        "processing_time": round(processing_time, 3)
    }

# FastAPI 앱 생성
app = FastAPI(
    title="AI 감정분석 서비스 (데모)",
    description="간단한 규칙 기반 감정분석 API 데모",
    version="1.0.0-demo"
)

@app.get("/", summary="Root endpoint")
async def root():
    return {
        "message": "AI 감정분석 서비스 데모",
        "version": "1.0.0-demo",
        "docs": "/docs",
        "health": "/health",
        "note": "이것은 실제 AI 모델 대신 규칙 기반 데모입니다"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0-demo",
        model_loaded=True
    )

@app.post("/predict", response_model=PredictResponse)
async def predict_sentiment(request: PredictRequest):
    try:
        result = analyze_sentiment_simple(request.text)
        return PredictResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 실패: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    return {
        "model_name": "simple-rule-based-demo",
        "model_type": "규칙 기반",
        "cache_dir": "N/A",
        "max_text_length": 512,
        "device": "cpu",
        "loaded": True,
        "note": "실제 AI 모델 대신 간단한 규칙을 사용합니다"
    }

if __name__ == "__main__":
    print("=" * 50)
    print("AI 감정분석 서비스 데모 시작")
    print("=" * 50)
    print("서비스 URL: http://localhost:8000")
    print("API 문서: http://localhost:8000/docs")
    print("헬스체크: http://localhost:8000/health")
    print("참고: 실제 AI 모델 대신 규칙 기반 데모입니다")
    print("=" * 50)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )