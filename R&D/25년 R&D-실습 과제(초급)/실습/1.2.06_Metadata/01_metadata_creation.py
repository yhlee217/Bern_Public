"""
실습: 메타데이터 생성 및 관리
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
import json

def create_metadata(doc_id, text, source, category):
    """문서 메타데이터 생성"""
    metadata = {
        'document_id': doc_id,
        'text': text,
        'source': source,
        'category': category,
        'created_at': datetime.now().isoformat(),
        'char_count': len(text),
        'word_count': len(text.split()),
        'language': 'ko'
    }
    return metadata

def add_quality_score(metadata, text):
    """품질 점수 추가"""
    score = min(100, len(text) // 10)  # 간단한 점수 계산
    metadata['quality_score'] = score
    return metadata

if __name__ == '__main__':
    # 샘플 문서
    doc = {
        'id': 'DOC_001',
        'text': '스마트팜은 ICT 기술을 활용하여 농작물 생육을 자동 제어하는 시스템입니다.',
        'source': 'smartfarm_guide.pdf',
        'category': '기술'
    }

    # 메타데이터 생성
    metadata = create_metadata(
        doc['id'],
        doc['text'],
        doc['source'],
        doc['category']
    )

    # 품질 점수 추가
    metadata = add_quality_score(metadata, doc['text'])

    print("=== 생성된 메타데이터 ===\n")
    print(json.dumps(metadata, indent=2, ensure_ascii=False))

    print(f"\n메타데이터 필드 수: {len(metadata)}")
    print(f"문서 품질 점수: {metadata['quality_score']}")
