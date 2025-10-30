# Docker 학습내용

## 1. Docker 기본 개념

### 1.1 Docker란?
- **컨테이너 기반 가상화 플랫폼**: 애플리케이션을 격리된 환경에서 실행
- **재현성**: 어떤 환경에서도 동일하게 동작
- **이식성**: 개발 환경과 프로덕션 환경의 차이 제거
- **격리성**: 각 컨테이너는 독립된 파일시스템과 프로세스 공간 보유

### 1.2 Docker vs 가상머신 (VM)
| 구분 | Docker | 가상머신 |
|------|--------|---------|
| 격리 수준 | 프로세스 레벨 | OS 레벨 |
| 성능 | 빠름 (네이티브에 가까움) | 느림 (하이퍼바이저 오버헤드) |
| 리소스 사용 | 적음 | 많음 (OS 전체 포함) |
| 시작 시간 | 초 단위 | 분 단위 |
| 이미지 크기 | MB ~ GB | GB ~ TB |

---

## 2. Docker 핵심 구성요소

### 2.1 Dockerfile
**정의**: Docker 이미지 빌드를 위한 설정 파일

**주요 명령어**:
```dockerfile
FROM python:3.11-slim          # 베이스 이미지
WORKDIR /app                   # 작업 디렉토리 설정
COPY requirements.txt .        # 파일 복사
RUN pip install -r requirements.txt  # 명령 실행
CMD ["python", "main.py"]      # 컨테이너 시작 명령
EXPOSE 8000                    # 포트 노출
ENV API_KEY=default            # 환경변수 설정
```

**멀티스테이지 빌드**:
```dockerfile
# Stage 1: 빌드 단계
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: 실행 단계 (경량화)
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
CMD ["python", "src/main.py"]
```

**장점**: 최종 이미지 크기 감소 (불필요한 빌드 도구 제외)

### 2.2 Docker Compose
**정의**: 여러 컨테이너를 한 번에 정의하고 실행하는 도구

**docker-compose.yml 예시**:
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MODEL_NAME=cardiffnlp/twitter-roberta-base-sentiment-latest
      - LOG_LEVEL=INFO
    volumes:
      - ./src:/app/src
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**주요 명령어**:
```bash
docker-compose up              # 서비스 시작
docker-compose up --build      # 빌드 후 시작
docker-compose up -d           # 백그라운드 실행
docker-compose down            # 서비스 종료 및 삭제
docker-compose logs -f         # 로그 확인
docker-compose ps              # 실행 중인 컨테이너 확인
```

### 2.3 헬스체크 (Health Check)
**목적**: 컨테이너 상태 모니터링 및 자동 복구

**Dockerfile에서 설정**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**의미**:
- `interval`: 30초마다 헬스체크 실행
- `timeout`: 10초 이내 응답 없으면 실패
- `retries`: 3회 연속 실패 시 unhealthy 상태

---

## 3. Docker 네트워킹

### 3.1 네트워크 모드
- **Bridge** (기본): 컨테이너 간 내부 네트워크 생성
- **Host**: 호스트 네트워크 직접 사용
- **None**: 네트워크 없음

### 3.2 포트 매핑
```bash
docker run -p 8000:8000 my-app
# 호스트:컨테이너
# 외부 8000 포트 → 컨테이너 내부 8000 포트
```

---

## 4. Docker 볼륨 (Volume)

### 4.1 데이터 영속성
**문제**: 컨테이너 삭제 시 데이터도 삭제됨
**해결**: 볼륨 사용으로 데이터 영속화

**방법**:
```yaml
volumes:
  - ./src:/app/src           # Bind Mount (개발용)
  - model-data:/app/models   # Named Volume (프로덕션용)

volumes:
  model-data:                # Volume 정의
```

### 4.2 Bind Mount vs Volume
| 구분 | Bind Mount | Named Volume |
|------|-----------|--------------|
| 위치 | 호스트 경로 지정 | Docker 관리 |
| 사용 사례 | 개발 (코드 변경 즉시 반영) | 프로덕션 (데이터 백업) |
| 성능 | OS에 따라 다름 | 일관성 있음 |

---

## 5. Docker 이미지 최적화

### 5.1 이미지 크기 줄이기
1. **경량 베이스 이미지 사용**
   ```dockerfile
   FROM python:3.11-slim  # slim 버전 사용 (full 대비 50% 감소)
   ```

2. **불필요한 파일 제외** (.dockerignore)
   ```
   __pycache__/
   *.pyc
   .git/
   tests/
   README.md
   ```

3. **레이어 캐싱 활용**
   ```dockerfile
   # ✅ 좋은 예: 변경 빈도가 낮은 것부터 먼저
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY src/ ./src/

   # ❌ 나쁜 예: 변경 빈도가 높은 것부터
   COPY . .
   RUN pip install -r requirements.txt
   ```

---

## 6. Makefile 자동화

### 6.1 Makefile이란?
**정의**: 반복적인 명령어를 자동화하는 스크립트

**예시**:
```makefile
.PHONY: build up down test lint

build:
	docker-compose -f docker/docker-compose.yml build

up:
	docker-compose -f docker/docker-compose.yml up -d

down:
	docker-compose -f docker/docker-compose.yml down

test:
	python -m pytest tests/ -v

lint:
	flake8 src/ tests/
	black --check src/ tests/

logs:
	docker-compose -f docker/docker-compose.yml logs -f
```

**사용법**:
```bash
make build    # 이미지 빌드
make up       # 서비스 시작
make test     # 테스트 실행
make down     # 서비스 종료
```

---

## 7. WSL2 (Windows Subsystem for Linux)

### 7.1 WSL2란?
- **Windows에서 Linux 실행**: 가상머신 없이 Linux 커널 실행
- **Docker Desktop 백엔드**: Windows에서 Docker 실행 시 WSL2 사용

### 7.2 WSL2 설정
```powershell
# WSL2 활성화
wsl --install

# Ubuntu 설치
wsl --install -d Ubuntu

# Docker Desktop 설정에서 WSL2 백엔드 활성화
```

### 7.3 장점
- 파일 시스템 성능 향상
- 네이티브 Linux 바이너리 실행
- Windows와 Linux 파일 공유

---

## 8. 환경변수 관리

### 8.1 .env 파일
**목적**: 민감한 정보와 환경별 설정 분리

**.env 예시**:
```bash
MODEL_NAME=cardiffnlp/twitter-roberta-base-sentiment-latest
LOG_LEVEL=INFO
API_PORT=8000
```

**.env.example** (Git 커밋용):
```bash
MODEL_NAME=your-model-name
LOG_LEVEL=INFO
API_PORT=8000
```

### 8.2 Docker Compose에서 사용
```yaml
services:
  api:
    env_file:
      - .env
    # 또는
    environment:
      - MODEL_NAME=${MODEL_NAME}
      - LOG_LEVEL=${LOG_LEVEL}
```

---

## 9. 보안 모범 사례

### 9.1 비밀정보 보호
- ✅ `.env` 파일 `.gitignore`에 추가
- ✅ `.env.example`로 필요한 변수 목록만 공유
- ❌ 절대 코드에 API 키 하드코딩 금지

### 9.2 최소 권한 원칙
```dockerfile
# ❌ root 사용자로 실행 (보안 취약)
CMD ["python", "main.py"]

# ✅ 일반 사용자 생성 후 실행
RUN useradd -m appuser
USER appuser
CMD ["python", "main.py"]
```

---

## 10. 학습 성과

### 완료한 개념
- ✅ Docker 기본 개념 및 아키텍처
- ✅ Dockerfile 작성 (멀티스테이지 빌드)
- ✅ Docker Compose 구성
- ✅ 헬스체크 구현
- ✅ 볼륨 관리 및 데이터 영속성
- ✅ 네트워킹 및 포트 매핑
- ✅ Makefile 자동화
- ✅ WSL2 환경 구축
- ✅ 환경변수 관리
- ✅ 보안 모범 사례

### 실습 시간
**총 8시간** (이론 3시간 + 실습 5시간)
