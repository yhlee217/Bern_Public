# Analysis Results

이 폴더에는 카카오톡 대화 감정 분석 결과가 저장됩니다.

## 📊 생성되는 파일

분석 실행 후 다음 파일들이 생성됩니다:

### 전체 분석 결과
- `full_kakaotalk_analysis_report.md` - 전체 분석 리포트
- `full_kakaotalk_analysis_data.json` - 전체 분석 데이터 (19,254개 메시지)

### 샘플 분석 결과
- `kakaotalk_analysis_report.md` - 샘플 리포트 (1,000개)
- `kakaotalk_analysis_data.json` - 샘플 데이터

## 🚀 분석 실행 방법

```bash
# 전체 분석 (약 26분 소요)
python analysis_scripts/full_analysis.py

# 샘플 분석 (약 79초 소요)
python analysis_scripts/batch_analyze_kakaotalk.py
```

## 📝 참고사항

- `.json` 파일은 용량이 크므로 Git에 커밋되지 않습니다
- `.md` 리포트 파일은 Git에 포함됩니다
- 분석 결과 샘플은 `docs/` 폴더에서 확인하세요
