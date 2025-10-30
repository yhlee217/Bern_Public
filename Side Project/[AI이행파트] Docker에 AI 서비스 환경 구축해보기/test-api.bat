@echo off
echo =====================================
echo AI 감정분석 API 테스트 스크립트
echo =====================================

REM PowerShell 사용 가능 여부 확인
powershell -Command "Write-Host 'PowerShell 준비 완료'" >nul 2>&1
if errorlevel 1 (
    echo [경고] PowerShell을 사용할 수 없습니다.
    echo 수동으로 브라우저에서 http://localhost:8000/docs 를 열어서 테스트해주세요.
    pause
    exit /b 1
)

echo.
echo 서비스 상태 확인 중...

REM 헬스체크
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method GET -TimeoutSec 5; Write-Host '✓ 서비스가 정상 실행 중입니다'; Write-Host \"상태: $($response.status)\"; Write-Host \"버전: $($response.version)\"; } catch { Write-Host '✗ 서비스에 연결할 수 없습니다. 서비스가 실행 중인지 확인해주세요.'; exit 1 }"

if errorlevel 1 (
    echo.
    echo 서비스가 실행되지 않았습니다.
    echo run.bat을 먼저 실행해주세요.
    pause
    exit /b 1
)

echo.
echo =====================================
echo 감정분석 테스트를 시작합니다
echo =====================================

:test_loop
echo.
set /p text="분석할 텍스트를 입력하세요 (종료: exit): "

if "%text%"=="exit" goto :end

if "%text%"=="" (
    echo 텍스트를 입력해주세요.
    goto :test_loop
)

echo.
echo 분석 중...

REM JSON 이스케이프 처리를 위해 PowerShell 사용
powershell -Command "$text = '%text%'; $body = @{ text = $text } | ConvertTo-Json; try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/predict' -Method POST -Body $body -ContentType 'application/json' -TimeoutSec 10; Write-Host \"📊 분석 결과:\"; Write-Host \"   감정: $($response.sentiment)\"; Write-Host \"   신뢰도: $([math]::Round($response.confidence * 100, 1))%%\"; Write-Host \"   처리시간: $($response.processing_time)초\"; } catch { Write-Host \"❌ 분석 실패: $($_.Exception.Message)\"; }"

goto :test_loop

:end
echo.
echo 테스트를 종료합니다.
echo.
echo 추가 기능:
echo - API 문서: http://localhost:8000/docs
echo - 고급 테스트: http://localhost:8000/redoc
pause