# 감정분석 모델 테스트 스크립트
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  감정분석 모델 테스트 (개선 버전)" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. 헬스체크
Write-Host "[1] 헬스체크" -ForegroundColor Yellow
$health = Invoke-RestMethod -Uri "http://localhost:8000/health"
Write-Host "상태: $($health.status)"
Write-Host "모델 로드: $($health.model_loaded)"
Write-Host "버전: $($health.version)"
Write-Host ""

# 2. 한글 긍정 테스트
Write-Host "[2] 한글 긍정 테스트" -ForegroundColor Green
$body = @{ text = "오늘 정말 기분이 좋다!" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
Write-Host "텍스트: 오늘 정말 기분이 좋다!"
Write-Host "감정: $($result.sentiment)"
Write-Host "신뢰도: $($result.confidence)"
Write-Host "처리시간: $($result.processing_time)초"
if ($result.model) { Write-Host "모델: $($result.model)" }
Write-Host ""

# 3. 한글 부정 테스트
Write-Host "[3] 한글 부정 테스트" -ForegroundColor Red
$body = @{ text = "정말 최악의 하루였어" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
Write-Host "텍스트: 정말 최악의 하루였어"
Write-Host "감정: $($result.sentiment)"
Write-Host "신뢰도: $($result.confidence)"
Write-Host "처리시간: $($result.processing_time)초"
Write-Host ""

# 4. 한글 중립 테스트
Write-Host "[4] 한글 중립 테스트" -ForegroundColor Yellow
$body = @{ text = "오늘 날씨가 흐립니다" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
Write-Host "텍스트: 오늘 날씨가 흐립니다"
Write-Host "감정: $($result.sentiment)"
Write-Host "신뢰도: $($result.confidence)"
Write-Host "처리시간: $($result.processing_time)초"
Write-Host ""

# 5. 영어 긍정 테스트
Write-Host "[5] 영어 긍정 테스트" -ForegroundColor Green
$body = @{ text = "I am very happy today!" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
Write-Host "텍스트: I am very happy today!"
Write-Host "감정: $($result.sentiment)"
Write-Host "신뢰도: $($result.confidence)"
Write-Host "처리시간: $($result.processing_time)초"
Write-Host ""

# 6. 영어 부정 테스트
Write-Host "[6] 영어 부정 테스트" -ForegroundColor Red
$body = @{ text = "This is terrible" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
Write-Host "텍스트: This is terrible"
Write-Host "감정: $($result.sentiment)"
Write-Host "신뢰도: $($result.confidence)"
Write-Host "처리시간: $($result.processing_time)초"
Write-Host ""

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  테스트 완료!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
