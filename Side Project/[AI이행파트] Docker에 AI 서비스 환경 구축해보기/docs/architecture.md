# 시스템 아키텍처

## 전체 시스템 구조

```mermaid
graph TB
    A[Client/Browser] -->|HTTP Request| B[FastAPI Server]
    B -->|Load Model| C[Hugging Face Model]
    C -->|Prediction| B
    B -->|JSON Response| A

    subgraph "Docker Container"
        B
        C
        D[Health Check]
    end

    E[Docker Compose] --> B
    F[Makefile] --> E
```

## API 엔드포인트

### 1. Health Check
- **URL**: `GET /health`
- **응답**: `{"status": "healthy", "timestamp": "2025-09-27T14:00:00Z"}`

### 2. 감정 분석
- **URL**: `POST /predict`
- **요청**:
  ```json
  {
    "text": "오늘 정말 기분이 좋다!"
  }
  ```
- **응답**:
  ```json
  {
    "sentiment": "positive",
    "confidence": 0.95,
    "processing_time": 0.12
  }
  ```

## 데이터 플로우

```mermaid
sequenceDiagram
    participant C as Client
    participant A as FastAPI
    participant M as AI Model

    C->>A: POST /predict {"text": "입력텍스트"}
    A->>A: 입력 검증
    A->>M: 텍스트 전처리 & 추론
    M->>A: 감정 분류 결과
    A->>C: JSON 응답 반환
```

## 기술 스택

- **웹 프레임워크**: FastAPI
- **AI/ML**: Hugging Face Transformers, PyTorch
- **컨테이너화**: Docker, Docker Compose
- **자동화**: Makefile
- **테스트**: pytest
- **문서화**: OpenAPI/Swagger