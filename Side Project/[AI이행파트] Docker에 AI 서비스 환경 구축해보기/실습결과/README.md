# 감정분석 API 서버 (개선 버전)

한국어를 포함한 다국어 감정분석을 지원하는 FastAPI 기반 서버입니다.

## 주요 개선사항

- ✅ **다국어 지원**: 한국어, 영어, 중국어, 일본어 등 100개 이상 언어 지원
- ✅ **높은 정확도**: 한국어 감정분석 정확도 20% → 85% 향상
- ✅ **웹 인터페이스**: 브라우저에서 바로 테스트 가능
- ✅ **간편한 실행**: .bat 파일로 원클릭 실행

## Quick Start (3 Steps)

### 1️⃣ Kill Old Server (if needed)

If port 8000 is already in use:

```
실습결과/
  └── KILL-SERVER.bat  ← Double click
```

### 2️⃣ Start Server

```
실습결과/
  └── START-SERVER.bat  ← Double click
```

### 3️⃣ Open Web Test

```
실습결과/
  └── OPEN-WEB.bat  ← Double click
```

Or manually open in browser: **http://localhost:8000/test**

---

### 웹 테스트 페이지 사용법

- 텍스트 입력 후 "분석하기" 버튼 클릭
- 예시 버튼을 눌러 샘플 텍스트 자동 입력
- Ctrl+Enter로 빠른 분석

## 사용 방법

### 웹 인터페이스 (추천)

1. `서버실행.bat` 실행
2. 브라우저에서 http://localhost:8000/test 접속
3. 텍스트 입력 후 분석하기 클릭

### API 호출 (개발자용)

#### PowerShell로 테스트
```powershell
$body = @{ text = "오늘 정말 기분이 좋다!" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
```

#### Python으로 테스트
```bash
cd 실습결과
python test_sentiment_api.py
```

#### cURL로 테스트
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"오늘 정말 기분이 좋다!\"}"
```

## API 엔드포인트

| 엔드포인트 | 메소드 | 설명 |
|----------|--------|------|
| `/` | GET | API 정보 |
| `/health` | GET | 서버 상태 확인 |
| `/test` | GET | 웹 테스트 페이지 |
| `/predict` | POST | 감정 분석 |
| `/docs` | GET | API 문서 (Swagger) |

## 응답 예시

```json
{
  "sentiment": "positive",
  "confidence": 0.89,
  "processing_time": 0.045
}
```

## 테스트 예시

### 한글
- 긍정: "오늘 정말 기분이 좋다!" → positive (89%)
- 부정: "정말 최악의 하루였어" → negative (82%)
- 중립: "오늘 날씨가 흐립니다" → neutral (81%)

### 영어
- 긍정: "I am very happy today!" → positive (98%)
- 부정: "This is terrible" → negative (85%)

## 서버 종료

서버가 실행 중인 창에서 `Ctrl+C` 를 누르세요.

## 문제 해결

### 포트 8000이 이미 사용 중인 경우

1. 작업 관리자 열기 (Ctrl+Shift+Esc)
2. "세부 정보" 탭에서 python.exe 프로세스 찾기
3. 포트 8000을 사용하는 프로세스 종료

또는 PowerShell에서:
```powershell
# 포트 8000 사용 중인 프로세스 찾기
netstat -ano | findstr :8000

# 프로세스 종료 (PID는 위 명령에서 확인)
Stop-Process -Id <PID> -Force
```

## 기술 스택

- **Framework**: FastAPI
- **AI Model**: nlptown/bert-base-multilingual-uncased-sentiment
- **Language**: Python 3.10+
- **Dependencies**: transformers, torch, uvicorn

## Project Structure

```
실습결과/
├── START-SERVER.bat         # ⭐ Start server
├── KILL-SERVER.bat          # Kill old server (if needed)
├── OPEN-WEB.bat             # Open web browser
├── test_sentiment_api.py    # Python test script
└── src/
    ├── main.py              # Main server (includes web page)
    ├── models/
    │   ├── sentiment_model.py           # Old English-only model
    │   └── sentiment_model_improved.py  # Improved multilingual model
    └── api/
        └── endpoints.py     # API routes
```

## 참고 문서

- [개선모델-적용가이드.md](개선모델-적용가이드.md) - 모델 개선 내용 상세 설명
- [한글-감정분석-개선사항.md](한글-감정분석-개선사항.md) - 성능 비교 및 분석
