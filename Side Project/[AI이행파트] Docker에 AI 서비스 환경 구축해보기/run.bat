@echo off
echo =====================================
echo AI 감정분석 서비스 실행 스크립트
echo =====================================

REM 환경변수 파일 설정
if not exist .env (
    echo .env 파일 생성 중...
    copy .env.example .env
    echo .env 파일이 생성되었습니다.
) else (
    echo .env 파일이 이미 존재합니다.
)

REM Docker 상태 확인
echo.
echo Docker 상태 확인 중...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [경고] Docker가 설치되지 않았거나 실행되지 않았습니다.
    echo Python 가상환경으로 실행합니다...
    goto :python_run
) else (
    echo Docker가 감지되었습니다.
    goto :docker_run
)

:docker_run
echo.
echo Docker Compose로 서비스 실행 중...
docker-compose -f docker/docker-compose.yml up --build
if errorlevel 1 (
    echo Docker 실행 실패. Python 가상환경으로 전환합니다...
    goto :python_run
) else (
    goto :success
)

:python_run
echo.
echo Python 가상환경 설정 중...

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되지 않았습니다.
    echo Python을 설치한 후 다시 실행해주세요.
    pause
    exit /b 1
)

REM 가상환경 생성
if not exist venv (
    echo 가상환경 생성 중...
    python -m venv venv
)

REM 가상환경 활성화
echo 가상환경 활성화 중...
call venv\Scripts\activate.bat

REM 의존성 설치
echo 의존성 설치 중... (시간이 걸릴 수 있습니다)
pip install -r requirements.txt

REM 서비스 실행
echo.
echo 서비스 실행 중...
cd src
python main.py

:success
echo.
echo =====================================
echo 서비스가 실행되었습니다!
echo.
echo 브라우저에서 다음 주소로 접속하세요:
echo - API 문서: http://localhost:8000/docs
echo - 헬스체크: http://localhost:8000/health
echo.
echo 종료하려면 Ctrl+C를 누르세요.
echo =====================================
pause