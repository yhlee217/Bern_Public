# 프로젝트 구조 가이드

**최종 업데이트**: 2025-10-08

---

## 📁 디렉토리 구조

```
E:\Side Project/
│
├── 📂 src/                          # AI 서비스 소스코드
│   ├── main.py                      # FastAPI 메인 애플리케이션
│   ├── api/                         # API 엔드포인트
│   │   ├── endpoints.py            # /predict, /predict/batch
│   │   └── schemas.py              # Pydantic 스키마
│   ├── models/                      # AI 모델
│   │   └── sentiment_model.py      # RoBERTa 감정 분석 모델
│   └── utils/                       # 유틸리티
│       └── config.py               # 설정 관리
│
├── 📂 analysis_scripts/             # 카카오톡 분석 스크립트
│   ├── analyze_kakaotalk.py        # 전체 분석 (초기 버전)
│   ├── analyze_kakaotalk_sample.py # 샘플 분석 (500개)
│   ├── batch_analyze_kakaotalk.py  # 배치 분석 (1,000개)
│   ├── full_analysis.py            # 전체 분석 (19,254개) ⭐
│   ├── quick_analyze.py            # 빠른 테스트 (50개)
│   └── visualize_analysis.py       # 시각화 생성 ⭐
│
├── 📂 results/                      # 분석 결과
│   ├── full_kakaotalk_analysis_report.md     # 전체 리포트 ⭐
│   ├── full_kakaotalk_analysis_data.json     # 전체 데이터 (3.8MB)
│   ├── kakaotalk_analysis_report.md          # 샘플 리포트
│   └── kakaotalk_analysis_data.json          # 샘플 데이터
│
├── 📂 visualizations/               # 시각화 (1,000개 샘플)
│   ├── sentiment_distribution.png
│   ├── sender_sentiment.png
│   ├── daily_activity.png
│   ├── hourly_heatmap.png
│   └── top_active_days.png
│
├── 📂 visualizations_full/          # 시각화 (19,254개 전체) ⭐
│   ├── sentiment_distribution.png   # 감정 분포 파이 차트
│   ├── sender_sentiment.png         # 발신자별 막대 그래프
│   ├── daily_activity.png           # 날짜별 활동 추이
│   ├── hourly_heatmap.png           # 시간대별 히트맵
│   └── top_active_days.png          # TOP 10 활발한 날
│
├── 📂 data/                         # 원본 데이터
│   └── KakaoTalk_예원.txt          # 카카오톡 대화 (23,990줄)
│
├── 📂 logs/                         # 작업 로그
│   └── daily/
│       ├── 2025-10-08.md                    # AI 서비스 실행 로그
│       ├── 2025-10-08-kakaotalk-analysis.md # 초기 분석 로그
│       ├── 2025-10-08-batch-optimization.md # 배치 최적화 로그
│       └── 2025-10-08-final-summary.md      # 최종 요약 ⭐
│
├── 📂 temp_files/                   # 임시 파일
│   ├── batch_analysis_log.txt
│   ├── full_analysis_log.txt
│   ├── kakaotalk_analysis_output.txt
│   └── test_batch.json
│
├── 📂 docker/                       # Docker 설정
│   ├── Dockerfile                   # 멀티스테이지 빌드
│   ├── docker-compose.yml
│   ├── entrypoint.sh
│   └── healthcheck.sh
│
├── 📂 tests/                        # 테스트 코드
│   ├── test_main.py
│   └── test_sentiment_model.py
│
├── 📂 docs/                         # 문서
│   └── architecture.md
│
├── 📂 models/                       # 모델 캐시
│   └── cache/
│
├── 📂 Report/                       # 리포트 (레거시)
│
├── 📄 README.md                     # 프로젝트 개요
├── 📄 PROJECT_STRUCTURE.md          # 본 문서 ⭐
├── 📄 AI_SERVICE_REPORT.md          # AI 서비스 보고서
├── 📄 REPORT.md                     # 과제 보고서
├── 📄 CHANGELOG.md                  # 변경 이력
├── 📄 USAGE.md                      # 사용법
├── 📄 DEPLOYMENT.md                 # 배포 가이드
├── 📄 EXPERIMENTS.md                # 실험 기록
├── 📄 RISKS.md                      # 리스크 관리
├── 📄 Guide.md                      # 개발 가이드
│
├── 📄 requirements.txt              # Python 패키지
├── 📄 Makefile                      # 빌드 자동화
├── 📄 LICENSE                       # MIT 라이선스
├── 📄 .env.example                  # 환경 변수 예시
├── 📄 run.bat                       # Windows 실행 스크립트
├── 📄 test-api.bat                  # API 테스트 스크립트
└── 📄 demo.py                       # 데모 스크립트
```

---

## 🎯 주요 파일 설명

### AI 서비스 관련

| 파일 | 설명 | 중요도 |
|-----|------|--------|
| `src/main.py` | FastAPI 메인 애플리케이션 | ⭐⭐⭐ |
| `src/api/endpoints.py` | API 엔드포인트 (배치 포함) | ⭐⭐⭐ |
| `src/models/sentiment_model.py` | RoBERTa 감정 분석 모델 | ⭐⭐⭐ |
| `requirements.txt` | Python 의존성 | ⭐⭐⭐ |

### 카카오톡 분석 관련

| 파일 | 설명 | 권장 사용 |
|-----|------|----------|
| `analysis_scripts/full_analysis.py` | 전체 분석 (19,254개) | ⭐⭐⭐ 프로덕션 |
| `analysis_scripts/visualize_analysis.py` | 시각화 생성 | ⭐⭐⭐ 프로덕션 |
| `analysis_scripts/batch_analyze_kakaotalk.py` | 배치 분석 (1,000개) | ⭐⭐ 테스트 |
| `analysis_scripts/quick_analyze.py` | 빠른 분석 (50개) | ⭐ 개발/디버그 |

### 결과 파일

| 파일 | 설명 | 크기 |
|-----|------|------|
| `results/full_kakaotalk_analysis_report.md` | 전체 분석 리포트 | ~8KB |
| `results/full_kakaotalk_analysis_data.json` | 전체 분석 데이터 | 3.8MB |
| `visualizations_full/*.png` | 시각화 차트 (5종) | ~1.2MB |

### 문서

| 파일 | 설명 |
|-----|------|
| `logs/daily/2025-10-08-final-summary.md` | 프로젝트 최종 요약 ⭐ |
| `logs/daily/2025-10-08-batch-optimization.md` | 배치 최적화 상세 로그 |
| `PROJECT_STRUCTURE.md` | 프로젝트 구조 가이드 (본 문서) |
| `README.md` | 프로젝트 개요 및 사용법 |

---

## 🚀 빠른 시작

### 1. AI 서비스 실행

```bash
# Windows
run.bat

# Linux/Mac
cd src && python main.py
```

서비스 URL: http://localhost:8000
API 문서: http://localhost:8000/docs

### 2. 카카오톡 분석 실행

```bash
# 전체 분석 (19,254개 메시지, ~26분 소요)
python analysis_scripts/full_analysis.py

# 빠른 테스트 (50개 메시지, ~30초 소요)
python analysis_scripts/quick_analyze.py
```

### 3. 시각화 생성

```bash
# 전체 데이터 기반 시각화
python analysis_scripts/visualize_analysis.py
```

결과: `visualizations_full/` 폴더에 5개 차트 생성

---

## 📊 분석 결과 확인

### 텍스트 리포트
```
results/full_kakaotalk_analysis_report.md
```

### 시각화 차트
```
visualizations_full/
  ├── sentiment_distribution.png    # 감정 분포
  ├── sender_sentiment.png          # 발신자별 통계
  ├── daily_activity.png            # 날짜별 추이
  ├── hourly_heatmap.png            # 시간대별 패턴
  └── top_active_days.png           # TOP 10 활발한 날
```

### JSON 데이터
```python
import json

# 전체 분석 데이터 로드
with open('results/full_kakaotalk_analysis_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"총 메시지: {len(data):,}개")
```

---

## 🔧 개발자 가이드

### 새로운 분석 스크립트 추가

1. `analysis_scripts/` 폴더에 스크립트 생성
2. 기존 스크립트 참고 (예: `full_analysis.py`)
3. 결과는 `results/` 폴더에 저장

### 새로운 시각화 추가

1. `visualize_analysis.py` 수정
2. matplotlib 함수 추가
3. `visualizations_full/` 폴더에 저장

### API 엔드포인트 추가

1. `src/api/schemas.py`에 스키마 정의
2. `src/api/endpoints.py`에 엔드포인트 추가
3. 서비스 재시작

---

## 📝 작업 로그 확인

모든 작업은 `logs/daily/` 폴더에 날짜별로 기록됩니다:

```
logs/daily/
  ├── 2025-10-08.md                    # AI 서비스 실행 로그
  ├── 2025-10-08-kakaotalk-analysis.md # 초기 분석 (50개 샘플)
  ├── 2025-10-08-batch-optimization.md # 배치 최적화 (1,000개)
  └── 2025-10-08-final-summary.md      # 최종 요약 (19,254개) ⭐
```

**추천 읽기 순서**:
1. `2025-10-08-final-summary.md` - 프로젝트 전체 요약
2. `results/full_kakaotalk_analysis_report.md` - 분석 결과
3. `visualizations_full/` - 시각화 차트

---

## 🎯 다음 단계

### 즉시 가능
- [ ] 웹 대시보드 개발 (FastAPI + React)
- [ ] 추가 시각화 (워드 클라우드, 네트워크 그래프)
- [ ] 실시간 분석 기능

### 단기 개선
- [ ] 한글 특화 모델 테스트 (KoBERT, KoELECTRA)
- [ ] 주제 모델링 추가
- [ ] 감정 강도 측정

### 중장기 계획
- [ ] GPU 지원
- [ ] 비동기 처리 (asyncio)
- [ ] 다국어 지원

---

## 💡 참고 자료

- **프로젝트 요약**: `logs/daily/2025-10-08-final-summary.md`
- **AI 서비스 사용법**: `README.md`
- **배포 가이드**: `DEPLOYMENT.md`
- **API 문서**: http://localhost:8000/docs (서비스 실행 중)

---

**프로젝트 상태**: ✅ 완료 (2025-10-08)
**메인테이너**: Development Team
**라이선스**: MIT
