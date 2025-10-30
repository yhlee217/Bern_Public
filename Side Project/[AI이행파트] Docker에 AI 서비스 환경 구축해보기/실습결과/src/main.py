from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
import os
from datetime import datetime
import logging
from contextlib import asynccontextmanager

from api.endpoints import router
# from models.sentiment_model import SentimentModel  # 기존 영어 전용 모델
from models.sentiment_model_improved import SentimentModelImproved as SentimentModel  # 개선된 다국어 모델
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
        "health": "/health",
        "test": "/test"
    }

# Web test page
@app.get("/test", response_class=HTMLResponse)
async def test_page():
    """Web-based test interface for sentiment analysis"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>감정분석 테스트 페이지</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .input-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 600;
            }
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
                resize: vertical;
                min-height: 120px;
                transition: border-color 0.3s;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            .button-group {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            button {
                flex: 1;
                padding: 15px;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            .btn-secondary {
                background: #f0f0f0;
                color: #333;
            }
            .btn-secondary:hover {
                background: #e0e0e0;
            }
            .examples {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin-bottom: 20px;
            }
            .example-btn {
                padding: 10px;
                background: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                font-size: 14px;
            }
            .example-btn:hover {
                background: #e9ecef;
                border-color: #667eea;
            }
            .result {
                margin-top: 20px;
                padding: 20px;
                border-radius: 10px;
                display: none;
            }
            .result.show {
                display: block;
            }
            .result.positive {
                background: #d4edda;
                border: 2px solid #28a745;
            }
            .result.negative {
                background: #f8d7da;
                border: 2px solid #dc3545;
            }
            .result.neutral {
                background: #fff3cd;
                border: 2px solid #ffc107;
            }
            .result-header {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .result-icon {
                font-size: 1.8em;
            }
            .result-details {
                color: #555;
                line-height: 1.8;
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            .loading.show {
                display: block;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .error {
                background: #f8d7da;
                border: 2px solid #dc3545;
                color: #721c24;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                display: none;
            }
            .error.show {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 감정분석 테스트</h1>
            <p class="subtitle">다국어 지원 감정분석 모델 (한국어/영어/중국어/일본어)</p>

            <div class="input-group">
                <label for="textInput">분석할 텍스트를 입력하세요</label>
                <textarea id="textInput" placeholder="예: 오늘 정말 기분이 좋다!"></textarea>
            </div>

            <div class="examples">
                <button class="example-btn" onclick="setExample('오늘 정말 기분이 좋다!')">😊 긍정 (한글)</button>
                <button class="example-btn" onclick="setExample('정말 최악의 하루였어')">😞 부정 (한글)</button>
                <button class="example-btn" onclick="setExample('오늘 날씨가 흐립니다')">😐 중립 (한글)</button>
                <button class="example-btn" onclick="setExample('I am very happy today!')">😊 긍정 (영어)</button>
                <button class="example-btn" onclick="setExample('This is terrible')">😞 부정 (영어)</button>
            </div>

            <div class="button-group">
                <button class="btn-primary" onclick="analyzeSentiment()">분석하기</button>
                <button class="btn-secondary" onclick="clearAll()">초기화</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 10px;">분석 중...</p>
            </div>

            <div class="result" id="result"></div>
            <div class="error" id="error"></div>
        </div>

        <script>
            function setExample(text) {
                document.getElementById('textInput').value = text;
            }

            function clearAll() {
                document.getElementById('textInput').value = '';
                document.getElementById('result').classList.remove('show');
                document.getElementById('error').classList.remove('show');
            }

            async function analyzeSentiment() {
                const text = document.getElementById('textInput').value.trim();
                const resultDiv = document.getElementById('result');
                const errorDiv = document.getElementById('error');
                const loadingDiv = document.getElementById('loading');

                if (!text) {
                    errorDiv.textContent = '텍스트를 입력해주세요.';
                    errorDiv.classList.add('show');
                    return;
                }

                // Hide previous results
                resultDiv.classList.remove('show', 'positive', 'negative', 'neutral');
                errorDiv.classList.remove('show');
                loadingDiv.classList.add('show');

                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: text })
                    });

                    if (!response.ok) {
                        throw new Error('분석 요청 실패');
                    }

                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    errorDiv.textContent = '오류 발생: ' + error.message;
                    errorDiv.classList.add('show');
                } finally {
                    loadingDiv.classList.remove('show');
                }
            }

            function displayResult(data) {
                const resultDiv = document.getElementById('result');
                const sentiment = data.sentiment;
                const confidence = (data.confidence * 100).toFixed(1);
                const processingTime = (data.processing_time * 1000).toFixed(0);

                let icon = '😐';
                let sentimentKo = '중립';
                let color = 'neutral';

                if (sentiment === 'positive') {
                    icon = '😊';
                    sentimentKo = '긍정';
                    color = 'positive';
                } else if (sentiment === 'negative') {
                    icon = '😞';
                    sentimentKo = '부정';
                    color = 'negative';
                }

                resultDiv.className = `result show ${color}`;
                resultDiv.innerHTML = `
                    <div class="result-header">
                        <span class="result-icon">${icon}</span>
                        <span>${sentimentKo}</span>
                    </div>
                    <div class="result-details">
                        <strong>감정:</strong> ${sentimentKo} (${sentiment})<br>
                        <strong>신뢰도:</strong> ${confidence}%<br>
                        <strong>처리시간:</strong> ${processingTime}ms
                    </div>
                `;
            }

            // Enter key to submit
            document.getElementById('textInput').addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    analyzeSentiment();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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