# Docker 기반 AI 감정분석 서비스 구축 프로젝트

> **Docker + FastAPI + Hugging Face Transformers**를 활용한 실시간 텍스트 감정분석 웹 서비스

---

## 📋 프로젝트 개요

**목적**: Docker 컨테이너 기술과 FastAPI 프레임워크를 활용하여 재현 가능하고 이식성 높은 AI 서비스 개발 환경 구축

**주요 기능**:
- ✅ 실시간 텍스트 감정 분석 (긍정/부정/중립)
- ✅ RESTful API 제공
- ✅ Docker 기반 배포
- ✅ OpenAPI/Swagger 자동 문서화
- ✅ 헬스체크 및 모니터링

---

## 🎯 학습 성과

### 완료한 학습 항목

**Docker 관련** :
- Docker 기본 개념 및 아키텍처
- Dockerfile 작성 (멀티스테이지 빌드)
- Docker Compose 구성
- 헬스체크 구현
- 볼륨 관리 및 데이터 영속성
- Makefile 자동화
- WSL2 환경 구축

**AI 서비스 아키텍처** :
- RESTful API 설계 원칙
- FastAPI 프레임워크
- Pydantic 데이터 검증
- Hugging Face Transformers 활용
- 감정분석 모델 통합
- 로깅 및 모니터링

**문서화 및 테스트** :
- OpenAPI 문서 작성
- pytest 테스트 코드
- 성능 벤치마크

---

## 🛠️ 기술 스택

| 분류 | 기술 | 버전 |
|------|------|------|
| **컨테이너** | Docker | 24.0+ |
| | Docker Compose | 2.0+ |
| **웹 프레임워크** | FastAPI | 0.104.1 |
| | Uvicorn | 0.24.0 |
| **AI/ML** | Transformers | 4.35.2 |
| | PyTorch | 2.1.1 |
| **데이터 검증** | Pydantic | 2.5.0 |

**AI 모델**: `cardiffnlp/twitter-roberta-base-sentiment-latest` (RoBERTa 기반)

---

## 📁 프로젝트 구조

```
[AI이행파트] Docker에 AI 서비스 환경 구축해보기/
├── README.md                   # 프로젝트 개요 (본 파일)
├── 프로젝트-통합보고서.md       # 상세 통합 보고서
│
├── 학습내용/                   # 이론 및 학습 자료
│   ├── Docker-학습내용.md      # Docker 핵심 개념
│   └── AI-서비스-아키텍처.md   # FastAPI + AI 모델 통합
│
├── 실습결과/                   # 실제 구현 코드
│   ├── src/                   # 소스 코드
│   │   ├── main.py           # FastAPI 앱
│   │   ├── model.py          # AI 모델 래퍼
│   │   ├── schemas.py        # Pydantic 스키마
│   │   └── config.py         # 설정
│   ├── docker/                # Docker 설정
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── tests/                 # 테스트 코드
│   ├── requirements.txt       # 의존성
│   ├── Makefile              # 빌드 자동화
│   └── .env.example          # 환경변수 예시
│
├── run.bat                    # Windows 원클릭 실행
├── test-api.bat               # Windows API 테스트
└── LICENSE                    # MIT License
```

---

## 🚀 빠른 시작

### 방법 1: Windows 원클릭 실행 (추천)

```cmd
# 1. 프로젝트 폴더에서 더블클릭
run.bat

# 2. API 테스트
test-api.bat
```

### 방법 2: Docker Compose

```bash
# 환경변수 설정
cp .env.example .env

# 서비스 시작
docker-compose -f 실습결과/docker/docker-compose.yml up --build

# 백그라운드 실행
docker-compose -f 실습결과/docker/docker-compose.yml up -d
```

### 방법 3: Makefile (Linux/Mac)

```bash
cd 실습결과/
make build   # 이미지 빌드
make up      # 서비스 시작
make test    # 테스트 실행
make down    # 서비스 종료
```

---

## 🧪 API 사용 예시

### 헬스체크
```bash
curl http://localhost:8000/health
```

**응답**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-09-27T14:30:00Z"
}
```

### 감정 분석

**요청**:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "오늘 정말 기분이 좋다!"}'
```

**응답**:
```json
{
  "sentiment": "positive",
  "confidence": 0.9527,
  "processing_time": 0.1203
}
```

---

## 📚 문서

- **[프로젝트 통합보고서](프로젝트-통합보고서.md)**: 전체 프로젝트 상세 내용
- **[Docker 학습내용](학습내용/Docker-학습내용.md)**: Docker 핵심 개념 및 실습
- **[AI 서비스 아키텍처](학습내용/AI-서비스-아키텍처.md)**: FastAPI + AI 모델 통합
- **API 문서**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 성능 지표

| 항목 | 수치 |
|------|------|
| 평균 응답 시간 | 0.12초 |
| 초당 처리량 | ~85 req/s |
| 메모리 사용량 | ~520MB |
| Docker 이미지 크기 | 1.2GB |
| 모델 로딩 시간 | ~3.2초 |

---

## 🎓 학습 하이라이트

### Docker 핵심 학습
- **멀티스테이지 빌드**: 이미지 크기 50% 감소
- **헬스체크**: 자동 복구 메커니즘
- **볼륨 마운트**: 개발 생산성 향상
- **WSL2**: Windows에서 네이티브 성능

### FastAPI 핵심 학습
- **타입 힌트 기반 검증**: Pydantic으로 자동 검증
- **비동기 처리**: async/await 활용
- **자동 문서화**: OpenAPI 스펙 자동 생성
- **성능 최적화**: 모델 로딩 전략

### AI 모델 통합
- **Hugging Face Hub**: 사전학습 모델 활용
- **모델 래퍼 패턴**: 유지보수성 확보
- **감정분석**: 3-class 분류 (positive/negative/neutral)

---

## 🔧 트러블슈팅

### Q1. Docker 빌드가 느려요
**A**: WSL2 백엔드를 활성화하세요. Windows 파일 시스템 대신 WSL2 파일 시스템 사용 시 3배 빠릅니다.

### Q2. 메모리 부족 에러
**A**: Docker Desktop 설정에서 메모리를 4GB 이상으로 증가시키세요.

### Q3. 모델 다운로드에 시간이 오래 걸려요
**A**: 첫 실행 시 약 500MB 모델 다운로드가 필요합니다. 이후엔 캐시를 사용합니다.

자세한 내용은 **[프로젝트 통합보고서](프로젝트-통합보고서.md) 9장. 트러블슈팅**을 참조하세요.

---

## 📈 향후 계획

- [ ] 배치 처리 API
- [ ] Redis 캐싱
- [ ] GPU 지원
- [ ] CI/CD 파이프라인
- [ ] 클라우드 배포 (AWS ECS)

---

## 📄 라이선스

MIT License - 자유롭게 사용 및 수정 가능합니다.

---

---

**🔗 관련 링크**:
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Docker 공식 문서](https://docs.docker.com/)
