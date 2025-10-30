# Baseline Parser 실습 예제

이 디렉토리는 Baseline Parser의 다양한 구현 예제와 테스트 데이터를 포함합니다.

## 📁 디렉토리 구조

```text
실습/
├── README.md                          # 이 파일
├── 01_simple_parser.py                # 단순 규칙 기반 문장 파서
├── 02_log_parser.py                   # 정규식 기반 로그 파서
├── 03_json_parser.py                  # JSON 검증 파서
├── 04_performance_comparison.py       # 성능 비교 벤치마크
└── data/                              # 테스트 데이터
    ├── sample_sentences.txt           # 샘플 문장 데이터
    ├── sample_logs.txt                # 샘플 로그 데이터
    └── sample_data.json               # 샘플 JSON 데이터
```

## 🚀 실행 방법

### 사전 준비

Python 3.6 이상이 설치되어 있어야 합니다.

```bash
# Python 버전 확인
python --version

# 또는
python3 --version
```

### 예제 실행

각 예제는 독립적으로 실행 가능합니다.

```bash
# 1. 단순 문장 파서
python 01_simple_parser.py

# 2. 로그 파서
python 02_log_parser.py

# 3. JSON 파서
python 03_json_parser.py

# 4. 성능 비교
python 04_performance_comparison.py
```

## 📚 예제 상세 설명

### 01_simple_parser.py - 단순 규칙 기반 문장 파서

**목적**: 품사 태그를 기반으로 문장의 기본 구조(주어, 술어, 수식어)를 파싱

**주요 기능**:
- POS 태그 기반 파싱
- 간단한 휴리스틱 파싱
- 파일에서 문장 읽어서 처리

**예제 출력**:
```text
문장 1: The cat runs quickly.
  주어(Subject):      cat
  술어(Predicate):    runs
  형용사(Adjectives): None
  부사(Adverbs):      quickly
  수식어(Modifiers):  The
```

**학습 포인트**:
- 가장 단순한 형태의 파서 구현
- 규칙 기반 접근법의 장단점 이해
- Baseline의 역할과 중요성

---

### 02_log_parser.py - 로그 파서

**목적**: 시스템 로그를 파싱하여 타임스탬프, 레벨, 메시지 추출

**주요 기능**:
- 다양한 로그 포맷 지원
- 로그 분석 통계
- 에러 로그 필터링
- 메타데이터 추출 (IP, 사용자, 경로)

**예제 출력**:
```text
원본: [2025-10-19 10:30:45] [ERROR] Database connection failed
  ├─ 타임스탬프: 2025-10-19 10:30:45
  ├─ 레벨:       ERROR
  └─ 메시지:     Database connection failed
```

**학습 포인트**:
- 정규식을 활용한 패턴 매칭
- 실제 운영 환경에서 사용 가능한 로그 파싱
- 로그 분석 및 통계 생성

---

### 03_json_parser.py - JSON 검증 파서

**목적**: JSON 데이터의 구조를 검증하고 스키마 준수 여부 확인

**주요 기능**:
- JSON 파싱 및 검증
- 스키마 기반 검증
- 데이터 타입 확인
- 필수 필드 검사
- 값 범위 검증

**예제 출력**:
```text
✅ 정상 데이터 검증:
  검증 성공!

❌ 필수 필드 누락:
  검증 실패:
    - root: 필수 필드 누락 'email'
```

**학습 포인트**:
- 데이터 품질 검증의 중요성
- 스키마 정의 및 활용
- 오류 처리 및 보고

---

### 04_performance_comparison.py - 성능 비교

**목적**: Baseline Parser와 개선된 Parser의 성능 비교

**주요 기능**:
- 파싱 속도 측정
- 정확도 비교
- 성능 벤치마크
- 여러 파서 동시 비교

**예제 출력**:
```text
📊 최종 비교 결과
Parser                    속도(ms)     주어성공률   술어성공률
----------------------------------------------------------------------
Baseline Parser           0.0125       100.0%       70.0%
Frequency-based Parser    0.0180       100.0%       85.0%
Rule-based Parser         0.0155       100.0%       90.0%
```

**학습 포인트**:
- Baseline의 성능 측정 방법
- 개선 효과 정량화
- 속도와 정확도의 트레이드오프

---

## 📊 테스트 데이터

### sample_sentences.txt

30개의 영어 문장으로 구성된 테스트 데이터입니다.

**용도**:
- 문장 파싱 테스트
- 파서 정확도 평가

**샘플**:
```text
The cat runs quickly.
A dog jumps over the fence.
The bird sings beautifully in the morning.
```

---

### sample_logs.txt

50개의 시스템 로그 라인으로 구성된 테스트 데이터입니다.

**용도**:
- 로그 파싱 테스트
- 로그 분석 실습

**로그 레벨 분포**:
- ERROR: ~30%
- WARNING: ~25%
- INFO: ~30%
- DEBUG: ~10%
- CRITICAL/FATAL: ~5%

**샘플**:
```text
[2025-10-19 10:30:45] [ERROR] Database connection failed
2025-10-19 10:31:22 INFO User admin logged in successfully
ERROR: 2025-10-19 10:32:10 - Invalid credentials for user: guest
```

---

### sample_data.json

전자상거래 시스템의 샘플 데이터입니다.

**구조**:
- `users`: 5명의 사용자 정보
- `products`: 5개의 제품 정보
- `orders`: 3개의 주문 정보
- `statistics`: 전체 통계

**용도**:
- JSON 파싱 테스트
- 스키마 검증 실습
- 복잡한 데이터 구조 처리

---

## 💡 학습 가이드

### 초급 학습 경로

1. **01_simple_parser.py 실행 및 이해**
   - 코드 읽기
   - 예제 실행
   - 다른 문장으로 테스트

2. **sample_sentences.txt 수정**
   - 새로운 문장 추가
   - 파싱 결과 관찰

3. **SimpleBaselineParser 클래스 수정**
   - 새로운 규칙 추가
   - 정확도 개선 시도

### 중급 학습 경로

1. **02_log_parser.py 분석**
   - 정규식 패턴 이해
   - 새로운 로그 포맷 추가

2. **03_json_parser.py 확장**
   - 새로운 스키마 정의
   - 추가 검증 규칙 구현

3. **성능 최적화**
   - 파싱 속도 개선
   - 메모리 사용량 최적화

### 고급 학습 경로

1. **04_performance_comparison.py 심화**
   - 새로운 파서 알고리즘 구현
   - 더 복잡한 벤치마크 작성

2. **실제 프로젝트 적용**
   - 실제 로그 파일로 테스트
   - 프로덕션 데이터 검증

3. **고급 파서로 발전**
   - 머신러닝 기반 파서
   - 신경망 파서

---

## 🛠️ 커스터마이징

### 새로운 파서 추가

```python
# my_custom_parser.py
class MyCustomParser:
    def __init__(self):
        # 초기화 코드
        pass

    def parse(self, data):
        # 파싱 로직
        return result

# 사용
parser = MyCustomParser()
result = parser.parse("test data")
```

### 새로운 테스트 데이터 추가

```bash
# data 디렉토리에 새 파일 생성
echo "새로운 테스트 데이터" > data/my_test_data.txt

# 파서에서 사용
with open('data/my_test_data.txt', 'r') as f:
    data = f.read()
```

---

## 📖 추가 학습 자료

### 권장 도서

- "Speech and Language Processing" - Jurafsky & Martin
- "Natural Language Processing with Python" - Bird, Klein & Loper
- "Foundations of Statistical NLP" - Manning & Schütze

### 온라인 리소스

- [Python 정규식 문서](https://docs.python.org/3/library/re.html)
- [JSON Schema 명세](https://json-schema.org/)
- [spaCy NLP 라이브러리](https://spacy.io/)

### 관련 GitHub 저장소

- [Drain3 로그 파서](https://github.com/logpai/Drain3)
- [Python JSON Schema](https://github.com/python-jsonschema/jsonschema)

---

## ❓ FAQ

### Q: Python 2에서도 실행 가능한가요?

A: 아니요, Python 3.6 이상이 필요합니다. f-string 등 Python 3 전용 기능을 사용합니다.

### Q: 외부 라이브러리가 필요한가요?

A: 기본 예제는 Python 표준 라이브러리만 사용합니다. 추가 라이브러리 없이 실행 가능합니다.

### Q: 실제 프로젝트에 사용할 수 있나요?

A: 이 예제들은 교육 목적입니다. 실제 프로젝트에서는 더 강력한 검증과 에러 처리가 필요합니다.

### Q: 한글 데이터도 처리할 수 있나요?

A: 로그 파서와 JSON 파서는 한글을 지원합니다. 문장 파서는 영어 중심이므로 한글 처리를 위해서는 수정이 필요합니다.

---

## 🤝 기여하기

개선 사항이나 버그를 발견하면 이슈를 등록하거나 풀 리퀘스트를 보내주세요.

---

## 📝 라이선스

이 예제 코드는 교육 목적으로 자유롭게 사용 가능합니다.

---

**작성일**: 2025-10-19
**버전**: 1.0
**문의**: R&D Team
