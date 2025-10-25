"""
실습: 코사인 유사도 기반 검색
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import math

def cosine_similarity(vec1, vec2):
    """코사인 유사도 계산"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (norm1 * norm2)

def vector_search(query_vec, doc_vecs, doc_texts, top_k=3):
    """벡터 검색"""
    similarities = []

    for i, doc_vec in enumerate(doc_vecs):
        sim = cosine_similarity(query_vec, doc_vec)
        similarities.append((i, sim, doc_texts[i]))

    # 유사도 순 정렬
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]

if __name__ == '__main__':
    # 샘플 문서 벡터 (단순화)
    doc_vecs = [
        [0.8, 0.2, 0.1],  # 문서1: 스마트팜 기술
        [0.3, 0.7, 0.2],  # 문서2: 센서 측정
        [0.1, 0.2, 0.9],  # 문서3: AI 예측
    ]

    doc_texts = [
        "스마트팜은 ICT 기술을 활용합니다",
        "센서로 환경을 측정합니다",
        "AI로 병충해를 예측합니다"
    ]

    # 쿼리 벡터
    query_vec = [0.7, 0.3, 0.1]  # "스마트팜 기술" 유사 쿼리

    print("=== 벡터 검색 결과 ===\n")
    print(f"쿼리 벡터: {query_vec}\n")

    results = vector_search(query_vec, doc_vecs, doc_texts, top_k=3)

    for rank, (doc_id, score, text) in enumerate(results, 1):
        print(f"[{rank}위] (유사도: {score:.4f})")
        print(f"  문서 {doc_id+1}: {text}")
        print()

    print("실제로는 Elasticsearch dense_vector 사용!")
