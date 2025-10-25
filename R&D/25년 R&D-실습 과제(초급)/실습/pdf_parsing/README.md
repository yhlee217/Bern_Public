# PDF 파싱 실습 가이드

이 디렉토리는 Python을 사용한 PDF 파일 파싱 실습을 위한 예제 코드를 포함하고 있습니다.

## 📋 목차

1. [환경 설정](#환경-설정)
2. [실습 파일 목록](#실습-파일-목록)
3. [실습 순서](#실습-순서)
4. [트러블슈팅](#트러블슈팅)

---

## 🛠️ 환경 설정

### 필수 라이브러리 설치

```bash
# 기본 PDF 처리
pip install PyPDF2

# 고급 텍스트 추출 및 테이블 파싱
pip install pdfplumber

# 고성능 PDF 처리 (선택사항)
pip install PyMuPDF

# 샘플 PDF 생성용
pip install reportlab

# 테이블 추출 (선택사항)
pip install tabula-py

# OCR (선택사항, 이미지 기반 PDF용)
pip install pytesseract
pip install pdf2image
```

### 시스템 요구사항

- Python 3.7 이상
- Windows, macOS, Linux

---

## 📚 실습 파일 목록

### 1. generate_sample_pdf.py
**샘플 PDF 파일 생성**

- 실습용 PDF 파일을 자동 생성
- 텍스트, 테이블이 포함된 다양한 PDF 생성
- **가장 먼저 실행해야 함**

```bash
python generate_sample_pdf.py
```

### 2. 01_basic_pdf_parser.py
**기본 PDF 파서 (PyPDF2)**

학습 내용:
- PDF 파일 열기 및 정보 읽기
- 텍스트 추출 기초
- PDF 파일 병합/분할
- 메타데이터 처리

```bash
python 01_basic_pdf_parser.py
```

### 3. 02_text_extractor.py
**텍스트 추출기 (pdfplumber)**

학습 내용:
- 정밀한 텍스트 추출
- 레이아웃 기반 파싱
- 영역 지정 추출
- 텍스트 분석

```bash
python 02_text_extractor.py
```

### 4. 03_table_extractor.py
**테이블 추출기 (pdfplumber)**

학습 내용:
- 테이블 자동 감지
- 테이블 데이터 DataFrame 변환
- CSV 저장
- 복잡한 테이블 처리

```bash
python 03_table_extractor.py
```

### 4. 04_image_extractor.py
**이미지 추출기 (PyMuPDF)**

학습 내용:
- PDF에서 이미지 추출
- 이미지 포맷 변환
- 이미지 메타데이터 확인

```bash
python 04_image_extractor.py
```

---

## 📖 실습 순서

### 단계 1: 샘플 PDF 생성

```bash
python generate_sample_pdf.py
```

실행 후 `data/` 디렉토리에 다음 파일이 생성됩니다:
- `sample.pdf`: 기본 텍스트 PDF
- `sample_table.pdf`: 테이블이 포함된 PDF

### 단계 2: 기본 파싱 실습

```bash
python 01_basic_pdf_parser.py
```

다음 기능을 테스트합니다:
- PDF 메타데이터 읽기
- 페이지별 텍스트 추출
- 전체 텍스트 추출
- PDF 분할

### 단계 3: 고급 텍스트 추출

```bash
python 02_text_extractor.py
```

다음 기능을 학습합니다:
- pdfplumber를 이용한 정밀 추출
- 좌표 기반 영역 추출
- 텍스트 검색 및 필터링

### 단계 4: 테이블 데이터 추출

```bash
python 03_table_extractor.py
```

다음 기능을 실습합니다:
- 테이블 자동 감지
- pandas DataFrame 변환
- CSV 파일로 저장
- 데이터 분석

### 단계 5: 이미지 추출 (선택사항)

```bash
python 04_image_extractor.py
```

이미지가 포함된 PDF가 있는 경우:
- PDF에서 이미지 추출
- 이미지 파일로 저장

---

## 🔍 트러블슈팅

### 문제 1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'PyPDF2'
```

**해결 방법:**
```bash
pip install PyPDF2 pdfplumber reportlab
```

### 문제 2: 한글이 추출되지 않음

**원인:**
- 폰트가 임베딩되지 않은 PDF
- 이미지 기반 PDF

**해결 방법:**
```python
# pdfplumber 사용
import pdfplumber
with pdfplumber.open('file.pdf') as pdf:
    text = pdf.pages[0].extract_text()

# 또는 OCR 사용 (이미지 기반 PDF)
# pip install pytesseract pdf2image
```

### 문제 3: 텍스트 순서가 뒤죽박죽

**원인:**
- 복잡한 레이아웃
- 다단 구조

**해결 방법:**
```python
# pdfplumber의 layout 모드 사용
with pdfplumber.open('file.pdf') as pdf:
    page = pdf.pages[0]
    text = page.extract_text(layout=True)
```

### 문제 4: 테이블이 감지되지 않음

**원인:**
- 선이 없는 테이블
- 복잡한 병합 셀

**해결 방법:**
```python
# 테이블 설정 조정
table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
}
tables = page.extract_tables(table_settings)

# 또는 camelot 사용
# pip install camelot-py[cv]
import camelot
tables = camelot.read_pdf('file.pdf', pages='1')
```

### 문제 5: 대용량 PDF 처리 시 메모리 부족

**해결 방법:**
```python
# 페이지별 처리
with pdfplumber.open('large.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        # 처리...

        # 메모리 해제
        if i % 10 == 0:
            import gc
            gc.collect()
```

---

## 📝 추가 학습 자료

### 공식 문서
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)

### 추천 튜토리얼
- [Real Python - Working with PDFs](https://realpython.com/pdf-python/)
- [DataCamp - PDF Processing](https://www.datacamp.com/tutorial/reading-pdfs-in-python)

### 관련 도구
- [PDF Debug Tool](https://github.com/pdfminer/pdfminer.six) - PDF 구조 분석
- [Tabula](https://tabula.technology/) - GUI 테이블 추출 도구
- [PDFtk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/) - PDF 조작 도구

---

## 💡 실전 응용 아이디어

1. **문서 자동화**
   - 청구서 정보 자동 추출
   - 계약서 데이터 파싱
   - 보고서 자동 생성

2. **데이터 마이그레이션**
   - 레거시 PDF를 데이터베이스로 이전
   - PDF를 Excel로 변환
   - 전자문서 아카이빙

3. **텍스트 분석**
   - PDF 문서 검색 시스템
   - 키워드 추출 및 분류
   - 문서 유사도 분석

4. **OCR 통합**
   - 스캔 문서 텍스트 추출
   - 이미지 기반 PDF 처리
   - 명함 정보 추출

---

## ❓ FAQ

**Q: PyPDF2와 pdfplumber 중 어떤 것을 사용해야 하나요?**

A:
- **PyPDF2**: 간단한 텍스트 추출, PDF 병합/분할
- **pdfplumber**: 테이블 추출, 정밀한 레이아웃 분석

**Q: 이미지 기반 PDF는 어떻게 처리하나요?**

A: OCR(Optical Character Recognition)을 사용해야 합니다.
```bash
pip install pytesseract pdf2image
```

**Q: 암호화된 PDF는 어떻게 열나요?**

A: PyPDF2의 decrypt 메서드 사용:
```python
reader.decrypt('password')
```

**Q: 대용량 PDF 처리 시 메모리가 부족합니다.**

A: 페이지별로 나누어 처리하고, 주기적으로 가비지 컬렉션을 수행하세요.

---

**작성자**: Bern
**버전**: 1.0
**최종 수정일**: 2025-10-23
