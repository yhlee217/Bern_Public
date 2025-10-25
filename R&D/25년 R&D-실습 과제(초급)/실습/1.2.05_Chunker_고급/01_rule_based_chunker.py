"""
실습: Rule-based Chunking (문장/문단 기준)
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re

def split_by_sentence(text):
    """문장 단위 분할"""
    pattern = r'([^.!?]*[.!?])\s*'
    sentences = re.findall(pattern, text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_by_sentences(text, max_size=500):
    """문장을 모아서 청크 생성"""
    sentences = split_by_sentence(text)
    chunks = []
    current = []
    current_len = 0

    for sent in sentences:
        if current_len + len(sent) <= max_size:
            current.append(sent)
            current_len += len(sent)
        else:
            if current:
                chunks.append(' '.join(current))
            current = [sent]
            current_len = len(sent)

    if current:
        chunks.append(' '.join(current))

    return chunks

if __name__ == '__main__':
    text = """스마트팜은 ICT 기술을 활용합니다. 센서로 환경을 측정합니다.
    자동으로 제어합니다! AI가 병충해를 예측합니다? 생산성이 향상됩니다."""

    print("=== 문장 기준 청킹 ===\n")
    chunks = chunk_by_sentences(text, max_size=100)

    for i, chunk in enumerate(chunks):
        print(f"[청크 {i+1}] ({len(chunk)}자)")
        print(chunk)
        print("-" * 50)

    print(f"\n총 {len(chunks)}개 청크 생성")
