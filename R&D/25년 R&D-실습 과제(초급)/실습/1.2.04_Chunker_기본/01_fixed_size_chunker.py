"""
실습 1: Fixed-size Chunking

목표:
- 고정 크기로 텍스트 분할
- 오버랩 적용
- 청크 메타데이터 관리
"""

import sys
import io

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def fixed_size_chunking(text, chunk_size=500, overlap=50):
    """고정 크기 청킹"""
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]

        if chunk_text.strip():
            chunks.append({
                'id': f'chunk_{chunk_id}',
                'text': chunk_text,
                'start': start,
                'end': min(end, len(text)),
                'length': len(chunk_text)
            })
            chunk_id += 1

        start += (chunk_size - overlap)

    return chunks


if __name__ == '__main__':
    # 샘플 텍스트
    sample_text = """
    스마트팜은 정보통신기술(ICT)을 활용하여 농작물의 생육 환경을 자동으로 제어하는 농업 방식입니다.
    센서를 통해 온도, 습도, CO2 농도, 일조량 등을 측정하고, 이 데이터를 기반으로 최적의 환경을 유지합니다.
    이를 통해 농작물의 생산성을 높이고, 노동력을 절감할 수 있습니다.
    최근에는 AI와 빅데이터를 결합하여 더욱 정밀한 농업이 가능해지고 있습니다.

    센서 기술은 스마트팜의 핵심 요소입니다. 온도 센서, 습도 센서, CO2 센서, 조도 센서 등 다양한 센서가 사용됩니다.
    이러한 센서들은 실시간으로 환경 데이터를 수집하고, 중앙 제어 시스템으로 전송합니다.
    제어 시스템은 수집된 데이터를 분석하여 최적의 환경을 유지하기 위한 명령을 내립니다.

    자동 제어 시스템은 관수, 양액 공급, 온도 조절, 환기 등을 자동으로 수행합니다.
    이를 통해 농부의 노동 시간이 크게 줄어들고, 일관된 품질의 농산물을 생산할 수 있습니다.
    """ * 3  # 텍스트를 3배로 늘림

    print(f"원본 텍스트 길이: {len(sample_text)} 문자\n")

    # 청킹 수행
    chunks = fixed_size_chunking(sample_text, chunk_size=300, overlap=50)

    print(f"총 청크 수: {len(chunks)}\n")

    # 결과 출력 (처음 3개만)
    for chunk in chunks[:3]:
        print(f"[{chunk['id']}] 위치: {chunk['start']}-{chunk['end']}")
        print(f"길이: {chunk['length']}자")
        print(f"내용: {chunk['text'][:80]}...")
        print("-" * 60)

    print(f"\n... (총 {len(chunks)}개 청크)")
