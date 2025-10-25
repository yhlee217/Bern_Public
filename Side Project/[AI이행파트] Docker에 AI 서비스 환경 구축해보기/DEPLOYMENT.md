# 배포 가이드

## 🖥️ 로컬 개발 환경

### 🚀 원클릭 실행 (Windows 추천)

```cmd
# 프로젝트 폴더에서 더블클릭하거나 실행
run.bat

# API 테스트
test-api.bat
```

**`run.bat` 기능:**
- 자동으로 Docker 또는 Python 환경 선택
- 환경변수 파일 자동 생성
- 의존성 자동 설치
- 서비스 자동 실행

### 1. Docker를 이용한 실행 (권장)

**Windows:**
```cmd
# 1. 프로젝트 디렉토리로 이동
cd "E:\Side Project"

# 2. 환경 설정
copy .env.example .env

# 3. 서비스 빌드 및 실행
docker-compose -f docker/docker-compose.yml up --build

# 4. 백그라운드 실행
docker-compose -f docker/docker-compose.yml up -d --build

# 5. 서비스 확인 (PowerShell)
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Linux/Mac:**
```bash
# 1. Docker Desktop 실행 확인
docker --version

# 2. 프로젝트 디렉토리로 이동
cd "E:\Side Project"

# 3. 환경 설정
cp .env.example .env

# 4. 서비스 빌드 및 실행
docker-compose -f docker/docker-compose.yml up --build

# 5. 서비스 확인
curl http://localhost:8000/health
```

### 2. Python 가상환경으로 실행

**Windows:**
```cmd
# 1. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정
copy .env.example .env

# 4. 서비스 실행
cd src
python main.py
```

**Linux/Mac:**
```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env

# 4. 서비스 실행
cd src
python main.py
```

## ☁️ 클라우드 배포

### 1. AWS ECS (Elastic Container Service)

```bash
# 1. AWS CLI 설정
aws configure

# 2. ECR 리포지토리 생성
aws ecr create-repository --repository-name ai-sentiment-service

# 3. Docker 이미지 빌드 및 푸시
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -f docker/Dockerfile -t ai-sentiment-service .
docker tag ai-sentiment-service:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-sentiment-service:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-sentiment-service:latest

# 4. ECS 서비스 생성 (task-definition.json 필요)
aws ecs create-service --cluster default --service-name ai-sentiment --task-definition ai-sentiment-task
```

### 2. Google Cloud Run

```bash
# 1. Google Cloud SDK 설정
gcloud auth login
gcloud config set project <project-id>

# 2. 이미지 빌드 및 배포
gcloud builds submit --tag gcr.io/<project-id>/ai-sentiment-service
gcloud run deploy ai-sentiment-service \
  --image gcr.io/<project-id>/ai-sentiment-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1
```

### 3. Heroku

```bash
# 1. Heroku CLI 설치 및 로그인
heroku login

# 2. 앱 생성
heroku create ai-sentiment-service

# 3. 컨테이너 배포
heroku container:login
heroku container:push web -a ai-sentiment-service
heroku container:release web -a ai-sentiment-service

# 4. 환경변수 설정
heroku config:set MODEL_NAME=cardiffnlp/twitter-roberta-base-sentiment-latest -a ai-sentiment-service
```

### 4. DigitalOcean App Platform

```bash
# 1. doctl CLI 설치 및 인증
doctl auth init

# 2. app.yaml 생성 후 배포
doctl apps create --spec app.yaml
```

## 🔧 환경별 설정

### 개발 환경 (.env)
```bash
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### 운영 환경 (.env.production)
```bash
DEBUG_MODE=false
LOG_LEVEL=INFO
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
MAX_WORKERS=4
REQUEST_TIMEOUT=30
```

## 📊 모니터링 및 로깅

### 1. 헬스체크 설정
```bash
# Docker Compose 헬스체크는 자동 설정됨
# 외부 모니터링 도구에서 사용:
curl -f http://your-domain.com/health
```

### 2. 로그 수집
```bash
# Docker 로그
docker-compose -f docker/docker-compose.yml logs -f

# 로그 수집 시스템 (예: ELK Stack)
# logstash.conf 설정 필요
```

## 🛡️ 보안 고려사항

### 1. HTTPS 설정 (Nginx 프록시)
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 환경변수 보안
- `.env` 파일을 git에 커밋하지 않음
- 클라우드 환경에서는 보안 저장소 사용 (AWS Secrets Manager, etc.)
- API 키나 토큰은 별도 관리

## 🔄 CI/CD 파이프라인

### GitHub Actions 예시 (.github/workflows/deploy.yml)
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build and Deploy
      run: |
        docker build -f docker/Dockerfile -t ai-sentiment .
        # 배포 스크립트 실행
```

## 📈 스케일링

### 1. 수평 확장
- 로드밸런서 뒤에 여러 인스턴스 배치
- Docker Swarm 또는 Kubernetes 사용

### 2. 성능 최적화
- 모델 캐싱 개선
- GPU 인스턴스 사용 고려
- 배치 처리 구현

## 🆘 트러블슈팅

### 자주 발생하는 문제
1. **메모리 부족**: 인스턴스 크기 증가 또는 모델 최적화
2. **응답 시간 초과**: 타임아웃 설정 조정
3. **모델 다운로드 실패**: 네트워크 설정 또는 프록시 확인

### 디버깅 명령어
```bash
# 컨테이너 로그 확인
docker logs <container-id>

# 컨테이너 내부 접속
docker exec -it <container-id> /bin/bash

# 리소스 사용량 확인
docker stats
```