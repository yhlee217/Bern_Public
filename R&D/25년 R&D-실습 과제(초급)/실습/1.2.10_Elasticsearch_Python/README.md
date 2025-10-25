# 1.2.10 Elasticsearch Python 실습

## 실습 파일
- `01_basic_operations.py` - 기본 CRUD 작업 (Mock)

## 실행
```bash
python 01_basic_operations.py
```

## 학습 내용
- Elasticsearch 기본 작업 흐름
- Index, Get, Search 이해
- Mock 객체로 개념 학습

## 실제 사용
Elasticsearch 서버 설치 후:
```python
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
```
