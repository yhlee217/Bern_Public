# 사용 가이드

## 🎯 빠른 시작

### 1. 서비스 실행 확인

**Windows (PowerShell):**
```powershell
# 헬스체크
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Windows (배치 스크립트):**
```cmd
# 프로젝트 폴더에서 실행
test-api.bat
```

**Linux/Mac:**
```bash
# 헬스체크
curl http://localhost:8000/health
```

**응답 예시:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-27T15:30:00Z",
  "version": "1.0.0",
  "model_loaded": true
}
```

### 2. API 문서 확인
브라우저에서 접속:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📱 API 사용법

### 1. 감정 분석 (기본)

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "오늘 정말 기분이 좋다!"}'
```

**응답:**
```json
{
  "sentiment": "positive",
  "confidence": 0.9234,
  "processing_time": 0.156
}
```

### 2. 다양한 텍스트 예시

**Windows (PowerShell):**
```powershell
# 긍정적 텍스트
$body = @{ text = "This product is amazing! I love it." } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"

# 부정적 텍스트
$body = @{ text = "이 제품은 정말 별로다. 실망했어요." } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"

# 중립적 텍스트
$body = @{ text = "오늘 날씨는 흐림입니다." } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method POST -Body $body -ContentType "application/json"
```

**Linux/Mac:**
```bash
# 긍정적 텍스트
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "This product is amazing! I love it."}'

# 부정적 텍스트
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "이 제품은 정말 별로다. 실망했어요."}'

# 중립적 텍스트
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "오늘 날씨는 흐림입니다."}'
```

### 3. 모델 정보 조회

```bash
curl http://localhost:8000/model/info
```

**응답:**
```json
{
  "model_name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
  "cache_dir": "./models/cache",
  "max_text_length": 512,
  "device": "cpu",
  "loaded": true
}
```

### 4. 모델 헬스체크

```bash
curl -X POST "http://localhost:8000/model/health"
```

**응답:**
```json
{
  "model_healthy": true,
  "status": "healthy"
}
```

## 💻 프로그래밍 언어별 예시

### Python
```python
import requests
import json

# API 엔드포인트
url = "http://localhost:8000/predict"

# 요청 데이터
data = {
    "text": "파이썬으로 API 호출하기!"
}

# POST 요청
response = requests.post(url, json=data)

# 결과 출력
if response.status_code == 200:
    result = response.json()
    print(f"감정: {result['sentiment']}")
    print(f"신뢰도: {result['confidence']:.2%}")
    print(f"처리시간: {result['processing_time']}초")
else:
    print(f"에러: {response.status_code}")
```

### JavaScript (Node.js)
```javascript
const axios = require('axios');

async function analyzeSentiment(text) {
  try {
    const response = await axios.post('http://localhost:8000/predict', {
      text: text
    });

    console.log('감정:', response.data.sentiment);
    console.log('신뢰도:', (response.data.confidence * 100).toFixed(1) + '%');
    console.log('처리시간:', response.data.processing_time + '초');

    return response.data;
  } catch (error) {
    console.error('에러:', error.response?.data || error.message);
  }
}

// 사용 예시
analyzeSentiment("JavaScript로 API 호출 성공!");
```

### JavaScript (브라우저)
```html
<!DOCTYPE html>
<html>
<head>
    <title>감정 분석 테스트</title>
</head>
<body>
    <input type="text" id="textInput" placeholder="분석할 텍스트를 입력하세요" style="width: 300px;">
    <button onclick="analyze()">분석하기</button>
    <div id="result"></div>

    <script>
    async function analyze() {
        const text = document.getElementById('textInput').value;
        const resultDiv = document.getElementById('result');

        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            const data = await response.json();

            resultDiv.innerHTML = `
                <h3>분석 결과:</h3>
                <p>감정: ${data.sentiment}</p>
                <p>신뢰도: ${(data.confidence * 100).toFixed(1)}%</p>
                <p>처리시간: ${data.processing_time}초</p>
            `;
        } catch (error) {
            resultDiv.innerHTML = `<p style="color: red;">에러: ${error.message}</p>`;
        }
    }
    </script>
</body>
</html>
```

### Java
```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import com.google.gson.Gson;
import java.util.Map;

public class SentimentAnalyzer {
    private static final String API_URL = "http://localhost:8000/predict";
    private static final HttpClient client = HttpClient.newHttpClient();
    private static final Gson gson = new Gson();

    public static void analyzeSentiment(String text) {
        try {
            // 요청 데이터 생성
            Map<String, String> requestData = Map.of("text", text);
            String jsonString = gson.toJson(requestData);

            // HTTP 요청 생성
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonString))
                .build();

            // 요청 전송
            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

            // 결과 파싱
            @SuppressWarnings("unchecked")
            Map<String, Object> result = gson.fromJson(response.body(), Map.class);

            System.out.println("감정: " + result.get("sentiment"));
            System.out.println("신뢰도: " + String.format("%.1f%%",
                (Double)result.get("confidence") * 100));
            System.out.println("처리시간: " + result.get("processing_time") + "초");

        } catch (Exception e) {
            System.err.println("에러: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        analyzeSentiment("Java로 API 호출 테스트!");
    }
}
```

## 📊 배치 처리 예시

### Python으로 여러 텍스트 처리
```python
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

def analyze_text(text):
    """단일 텍스트 분석"""
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def batch_analyze(texts, max_workers=5):
    """배치 분석"""
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(analyze_text, text) for text in texts]

        for i, future in enumerate(futures):
            result = future.result()
            result['original_text'] = texts[i]
            results.append(result)
            print(f"진행률: {i+1}/{len(texts)}")

    return results

# 사용 예시
texts = [
    "이 제품은 정말 훌륭합니다!",
    "배송이 너무 늦어서 실망했어요.",
    "가격대비 괜찮은 것 같아요.",
    "다시는 구매하지 않을 겁니다.",
    "추천하고 싶은 제품입니다."
]

start_time = time.time()
results = batch_analyze(texts)
end_time = time.time()

# 결과를 DataFrame으로 정리
df = pd.DataFrame(results)
print(f"\n총 처리 시간: {end_time - start_time:.2f}초")
print(f"평균 처리 시간: {df['processing_time'].mean():.3f}초")
print("\n결과 요약:")
print(df[['original_text', 'sentiment', 'confidence']].to_string(index=False))
```

## 🔍 에러 처리

### 일반적인 에러 응답
```json
// 400 Bad Request - 잘못된 입력
{
  "detail": "Input text cannot be empty"
}

// 422 Validation Error - 스키마 검증 실패
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

// 503 Service Unavailable - 모델 로딩 실패
{
  "detail": "Model not loaded"
}

// 500 Internal Server Error - 서버 오류
{
  "detail": "Prediction failed"
}
```

### 에러 처리 예시 (Python)
```python
def safe_analyze(text):
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"text": text},
            timeout=5
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            print(f"입력 오류: {response.json()['detail']}")
        elif response.status_code == 503:
            print("서비스가 일시적으로 사용할 수 없습니다.")
        else:
            print(f"서버 오류: {response.status_code}")

    except requests.exceptions.Timeout:
        print("요청 시간 초과")
    except requests.exceptions.ConnectionError:
        print("서버에 연결할 수 없습니다.")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

    return None
```

## 📈 성능 최적화 팁

1. **동시 요청 제한**: 서버 과부하 방지를 위해 동시 요청 수 제한
2. **타임아웃 설정**: 네트워크 지연을 고려한 적절한 타임아웃 설정
3. **재시도 로직**: 일시적 오류에 대한 재시도 메커니즘 구현
4. **캐싱**: 동일한 텍스트에 대한 결과 캐싱 고려