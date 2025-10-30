# 1.2.12 프롬프트 엔지니어링 실습

## 실습 파일

### 01_prompt_templates.py
- 재사용 가능한 프롬프트 템플릿
- 구조화된 프롬프트 패턴
- Few-shot 템플릿
- 프롬프트 라이브러리

## 실행 방법

```bash
python 01_prompt_templates.py
```

## 학습 내용

### 1. 구조화된 프롬프트
- 역할, 맥락, 작업, 제약조건, 출력 형식 명시
- 일관된 품질의 답변 생성

### 2. Few-shot Learning
- 예시를 통한 학습
- 원하는 형식 지정

### 3. 프롬프트 라이브러리
- 요약, 분류, 추출, Q&A 등 공통 태스크
- 재사용 가능한 템플릿

## 실전 활용

이 템플릿들을 OpenAI API 또는 다른 LLM과 함께 사용:

```python
from openai import OpenAI
client = OpenAI(api_key="your-key")

prompt = PromptLibrary.summarize(long_text, sentences=3)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
```

## 주요 학습 포인트

1. **명확한 지시**: 구체적일수록 좋은 결과
2. **Few-shot**: 예시로 형식 학습
3. **템플릿화**: 재사용성 향상
4. **구조화**: 일관성 유지
