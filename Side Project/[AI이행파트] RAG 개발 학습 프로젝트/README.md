# RAG 개발 학습 프로젝트

> **부서**: AI이행파트  
> **기간**: 2025년 10월  
> **학습 시간**: 32시간  
> **목표**: RAG 시스템 개발 역량 확보

---

## 📋 프로젝트 개요

AI이행파트의 RAG(Retrieval-Augmented Generation) 시스템 개발 역량 강화를 위한 **체계적 학습 프로젝트**입니다.

### 학습 방식
```
이론 학습 (R&D 문서) → 실습 구현 → 테스트 검증 → 결과 정리
```

### 학습 로드맵
```
1단계: 개발 환경 구축 (4시간)
   ↓
2단계: RAG 파이프라인 구현 (16시간)
   ↓
3단계: API 서버 개발 (12시간)
```

---

## 🎯 학습 성과 요약

| 단계 | 주제 | 실습 완료 | 학습 내용 |
|-----|------|----------|----------|
| **1단계** | 개발 환경 구축 | ✅ | Docker, VSCode, Elasticsearch |
| **2단계** | RAG 파이프라인 | ✅ | Parser, Chunker, Embedding, Vector Search, LLM |
| **3단계** | API 서버 개발 | ✅ | SQLAlchemy, FastAPI, 디자인패턴, Logging |

### 핵심 역량 향상

| 기술 분야 | 학습 전 | 학습 후 | 비고 |
|---------|---------|---------|------|
| **Docker** | 미경험 | 중급 | 컨테이너 구성 가능 |
| **RAG 파이프라인** | 미경험 | 중급 | 전체 흐름 이해 및 구현 |
| **FastAPI** | 초급 | 중급 | RESTful API 설계 가능 |
| **SQLAlchemy** | 미경험 | 초급 | ORM 기본 활용 가능 |

---

## 📂 프로젝트 구조

```
RAG 개발 학습 프로젝트/
│
├── README.md                    # 본 문서 (프로젝트 개요 및 성과)
│
├── 1.개발환경-구축/
│   ├── 학습내용/
│   │   └── 학습내용.md          # Docker, Elasticsearch 이론 정리
│   └── 실습결과/
│       └── docker-compose.yml   # Elasticsearch 구성 파일
│
├── 2.RAG-파이프라인-구현/
│   ├── 학습내용/
│   │   └── 학습내용.md          # Parser~LLM 이론 정리
│   └── 실습결과/
│       ├── Parser-실습/
│       ├── Chunker-실습/
│       ├── Embedding-실습/
│       ├── VectorSearch-실습/
│       ├── LLM-실습/
│       └── 테스트결과.md
│
└── 3.API-서버-개발/
    ├── 학습내용/
    │   └── 학습내용.md          # SQLAlchemy, FastAPI 이론 정리
    └── 실습결과/
        ├── SQLAlchemy-실습/
        ├── FastAPI-실습/
        └── 테스트결과.md
```

---

## 💡 1단계: 개발 환경 구축

### 학습 내용
- VSCode 개발 환경 설정
- Windows Docker CLI 설치 (WSL2)
- Elasticsearch & Kibana 구성

### 실습 성과
- ✅ Docker Compose로 Elasticsearch + Kibana 구성 완료
- ✅ Elasticsearch 정상 실행 (http://localhost:9200)
- ✅ Kibana 대시보드 접속 (http://localhost:5601)

---

## 💡 2단계: RAG 파이프라인 구현

### 2-1. Parser (문서 파싱)
**학습**: Baseline Parser, PDF/TXT 파싱  
**실습**: 4개 파서 구현 (Simple, Log, JSON, Performance)  
**성과**: ✅ PDF 100페이지 2.5초 처리

### 2-2. Chunker (텍스트 분할)
**학습**: Fixed-size, Rule-based 청킹  
**실습**: 2가지 청킹 기법 구현  
**성과**: ✅ 10,000자 문서 → 22개 청크 생성

### 2-3. Metadata (메타데이터)
**학습**: 메타데이터 구조, 품질 평가  
**실습**: 메타데이터 생성 및 품질 점수 계산  
**성과**: ✅ 품질 평가 시스템 구현

### 2-4. Embedding (벡터화)
**학습**: TF-IDF 벡터화 원리  
**실습**: TF-IDF 임베딩 구현  
**성과**: ✅ 1,000개 문서 3.5초 벡터화

### 2-5. Vector Search (벡터 검색)
**학습**: 코사인 유사도, Top-K 검색  
**실습**: 유사도 검색 알고리즘 구현  
**성과**: ✅ 1,000개 벡터 중 Top-5 검색 45ms

### 2-6. Elasticsearch 연동
**학습**: ES Python 클라이언트, 인덱싱  
**실습**: Mock Elasticsearch 클래스 구현  
**성과**: ✅ CRUD 작업 테스트 완료

### 2-7. LLM 호출
**학습**: OpenAI API, Prompt Engineering  
**실습**: LLM 호출 및 Few-shot Learning  
**성과**: ✅ API 연동 및 Temperature 테스트

---

## 💡 3단계: API 서버 개발

### 3-1. SQLAlchemy (ORM)
**학습**: ORM 개념, 모델 정의, CRUD  
**실습**: User 모델 생성 및 관계 설정  
**성과**: ✅ 1:N, N:M 관계 구현 완료

### 3-2. FastAPI (REST API)
**학습**: HTTP 메서드, Request/Response  
**실습**: CRUD API 구현  
**성과**: ✅ Swagger UI 자동 생성

### 3-3. 디자인 패턴
**학습**: Router-Service-Repository 패턴  
**실습**: 3계층 아키텍처 적용  
**성과**: ✅ 관심사 분리 구조 구현

### 3-4. Logging
**학습**: Python logging, 파일 로테이션  
**실습**: 로깅 시스템 구축  
**성과**: ✅ 요청/응답 로깅 미들웨어 적용

---

## 📊 실습 결과 요약

### 구현 완료 항목
- ✅ Parser: 4개 파일 (TXT, PDF, JSON, 성능비교)
- ✅ Chunker: 2개 기법 (Fixed-size, Rule-based)
- ✅ Metadata: 품질 평가 시스템
- ✅ Embedding: TF-IDF 벡터화
- ✅ Vector Search: 코사인 유사도 검색
- ✅ Elasticsearch: Mock 클래스
- ✅ LLM: OpenAI API 연동
- ✅ SQLAlchemy: ORM 기본 CRUD
- ✅ FastAPI: RESTful API 서버

### 성능 측정 결과

| 항목 | 결과 | 비고 |
|-----|------|------|
| PDF 파싱 속도 | 100페이지 / 2.5초 | PyPDF2 |
| 청킹 처리량 | 10,000자 / 0.1초 | Fixed-size |
| 벡터화 속도 | 1,000개 / 3.5초 | TF-IDF |
| 벡터 검색 | Top-5 / 45ms | 1,000개 중 |
| 검색 정확도 | 92% | Top-5 Recall |

---

## 🔧 기술 스택

### 환경
- OS: Windows 11
- IDE: VSCode
- Container: Docker Desktop

### Python 라이브러리
```
PyPDF2==3.0.1
scikit-learn==1.3.0
SQLAlchemy==2.0.23
fastapi==0.104.1
openai==1.3.0
```

---

## 📝 참고 자료

### 내부 학습 자료
- **R&D 폴더**: 상세 이론 및 가이드 (20개 문서)
  - 환경 설정 (1.1.01 ~ 1.1.05)
  - RAG 파이프라인 (1.2.01 ~ 1.2.12)
  - API 개발 (1.3.01 ~ 1.3.06)

### 실습 코드
- **R&D/실습 폴더**: 테스트 완료된 실습 코드
  - Parser, Chunker, Embedding, VectorSearch
  - Elasticsearch, LLM 호출
  - 압축 파일 (zip) 포함

---

## 🚀 향후 계획

### 단기 (1개월)
- [ ] Sentence Transformer 실습
- [ ] Elasticsearch 실제 서버 연동
- [ ] API 서버 Docker 컨테이너화

### 중기 (3개월)
- [ ] RAG 전체 파이프라인 통합
- [ ] 프로덕션 코드 작성
- [ ] 성능 최적화

---

**작성자**: AI이행파트  
**작성일**: 2025년 10월 26일  
**문서 유형**: 학습 프로젝트 보고서
