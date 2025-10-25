# AI 텍스트 감정 분석 서비스

Docker 기반의 실시간 텍스트 감정 분석 API 서비스입니다.

## 🎯 프로젝트 개요

이 프로젝트는 입력된 텍스트의 감정(긍정/부정/중립)을 분석하여 JSON 형태로 결과를 반환하는 RESTful API 서비스입니다.

### 주요 기능
- 실시간 텍스트 감정 분석
- RESTful API 제공
- Docker 기반 배포
- OpenAPI/Swagger 문서화

## 🚀 빠른 시작

### 💡 가장 쉬운 방법 (Windows)

1. **파일 탐색기**에서 프로젝트 폴더 열기
2. **`run.bat`** 더블클릭으로 실행
3. **`test-api.bat`** 더블클릭으로 API 테스트

### 필수 조건
- **Windows**: Python 또는 Docker Desktop
- **Linux/Mac**: Docker & Docker Compose, Python 3.10+

### 실행 방법

**Windows (추천):**
```cmd
# 원클릭 실행
run.bat

# API 테스트
test-api.bat
```

**수동 실행 (모든 OS):**
```bash
# 1. 환경 변수 설정
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 2. Docker로 실행
docker-compose -f docker/docker-compose.yml up --build

# 3. 또는 Python으로 실행
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cd src && python main.py
```

### 🧪 API 테스트

**PowerShell (Windows):**
```powershell
# 헬스체크
Invoke-RestMethod -Uri "http://localhost:8000/health"

# 감정분석
$body = @{ text = "오늘 정말 기분이 좋다!" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
```

**Curl (Linux/Mac):**
```bash
# 헬스체크
curl http://localhost:8000/health

# 감정분석
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "오늘 정말 기분이 좋다!"}'
```

## 📚 API 문서

서비스 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 주요 엔드포인트

#### 헬스체크
```bash
GET /health
```

#### 감정 분석
```bash
POST /predict
Content-Type: application/json

{
  "text": "분석할 텍스트"
}
```

**응답 예시:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "processing_time": 0.12
}
```

## 🏗️ 시스템 아키텍처

```
Client → FastAPI → AI Model → Response
           ↓
    Docker Container
```

자세한 아키텍처 정보는 [docs/architecture.md](docs/architecture.md)를 참조하세요.

## 🛠️ 개발

### 개발 환경 설정

**Windows:**
```cmd
# 개발 모드로 실행
docker-compose -f docker/docker-compose.yml up --build

# 테스트 실행 (가상환경에서)
venv\Scripts\activate
python -m pytest tests/ -v

# 코드 린팅 (가상환경에서)
python -m flake8 src/ tests/
python -m black --check src/ tests/
```

**Linux/Mac:**
```bash
# 개발 모드로 실행
make dev  # 또는 docker-compose -f docker/docker-compose.yml up --build

# 테스트 실행
make test  # 또는 python -m pytest tests/ -v

# 코드 린팅
make lint  # 또는 flake8 src/ tests/
```

### 프로젝트 구조

```
├── 📁 docker/          # 컨테이너 설정
├── 📁 src/             # 소스 코드 (3개 패키지)
├── 📁 tests/           # 테스트 코드
├── 📁 docs/            # 문서
├── 📁 logs/            # 작업 저널
├── 🐳 Dockerfile      # 멀티스테이지 빌드
├── 🔧 Makefile        # 자동화 스크립트
├── 📋 requirements.txt # 의존성 (17개 패키지)
└── 📚 README.md       # 프로젝트 가이드
```
