"""
실습: 간단한 임베딩 (TF-IDF 기반)
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collections import Counter
import math

def simple_embedding(text, vocab):
    """간단한 TF-IDF 임베딩"""
    words = text.lower().split()
    word_count = Counter(words)

    # TF 계산
    tf = {word: count / len(words) for word, count in word_count.items()}

    # 벡터 생성 (vocab 기준)
    vector = [tf.get(word, 0) for word in vocab]

    return vector

if __name__ == '__main__':
    # 샘플 문서
    docs = [
        "스마트팜은 ICT 기술을 활용합니다",
        "센서로 온도와 습도를 측정합니다",
        "AI 기술로 병충해를 예측합니다"
    ]

    # 전체 vocabulary 생성
    all_words = []
    for doc in docs:
        all_words.extend(doc.lower().split())

    vocab = sorted(set(all_words))

    print(f"Vocabulary 크기: {len(vocab)}")
    print(f"Vocabulary: {vocab}\n")

    # 각 문서 임베딩
    for i, doc in enumerate(docs):
        vec = simple_embedding(doc, vocab)
        print(f"문서 {i+1}: {doc}")
        print(f"벡터 (차원: {len(vec)}): {[round(v, 3) for v in vec[:5]]}...")
        print()

    print("실제로는 sentence-transformers 같은 고급 모델 사용 권장!")
