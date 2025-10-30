"""
실습 2: Chunker 클래스 구현

목표:
- 재사용 가능한 Chunker 클래스 작성
- 다양한 파라미터 지원
- 메타데이터 관리
"""

import sys
import io

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class SimpleChunker:
    """간단한 청커 구현 예시"""

    def __init__(self, chunk_size=500, overlap=100, separator='\n\n'):
        """
        Args:
            chunk_size: 청크의 최대 크기 (문자 수)
            overlap: 청크 간 중복 크기 (문자 수)
            separator: 우선 분할 기준 (문단, 문장 등)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator

    def chunk(self, text, metadata=None):
        """
        텍스트를 청크로 분할

        Args:
            text: 분할할 텍스트
            metadata: 원본 문서 메타데이터

        Returns:
            청크 리스트 (딕셔너리 형태)
        """
        chunks = []

        # 1. 먼저 separator로 분할
        segments = text.split(self.separator)

        current_chunk = ""
        chunk_index = 0

        for segment in segments:
            # 현재 청크에 세그먼트 추가 시 크기 확인
            if len(current_chunk) + len(segment) <= self.chunk_size:
                current_chunk += segment + self.separator
            else:
                # 현재 청크 저장
                if current_chunk.strip():
                    chunks.append({
                        'chunk_id': f'chunk_{chunk_index}',
                        'text': current_chunk.strip(),
                        'metadata': {
                            'chunk_index': chunk_index,
                            'char_count': len(current_chunk.strip()),
                            'original_metadata': metadata
                        }
                    })
                    chunk_index += 1

                # 새 청크 시작 (오버랩 적용)
                if self.overlap > 0 and current_chunk:
                    # 이전 청크의 마지막 일부를 포함
                    overlap_text = current_chunk[-self.overlap:]
                    current_chunk = overlap_text + segment + self.separator
                else:
                    current_chunk = segment + self.separator

        # 마지막 청크 저장
        if current_chunk.strip():
            chunks.append({
                'chunk_id': f'chunk_{chunk_index}',
                'text': current_chunk.strip(),
                'metadata': {
                    'chunk_index': chunk_index,
                    'char_count': len(current_chunk.strip()),
                    'original_metadata': metadata
                }
            })

        # 전체 청크 수 메타데이터 추가
        for chunk in chunks:
            chunk['metadata']['total_chunks'] = len(chunks)

        return chunks


if __name__ == '__main__':
    # Chunker 인스턴스 생성
    chunker = SimpleChunker(chunk_size=200, overlap=50, separator='\n\n')

    # 샘플 텍스트
    sample_text = """
제1장. 서론
본 연구는 스마트팜 기술의 현황과 발전 방향을 분석하고자 합니다.

제2장. 스마트팜 기술 개요
스마트팜은 IoT, AI, 빅데이터 등 첨단 기술을 활용하여 농작물의 생육 환경을 자동으로 제어하고 최적화하는 농업 시스템입니다.

제3장. 주요 기술 요소
환경 센서: 온도, 습도, CO2, 조도 등을 측정합니다.
자동 제어: 관수, 양액, 온도 등을 자동 조절합니다.
데이터 분석: 생육 데이터 수집 및 분석을 수행합니다.

제4장. 실증 사례
경기도 소재 A농장에서는 스마트팜 도입 후 생산성이 30% 향상되었습니다.
"""

    # 메타데이터
    metadata = {
        'source': 'smartfarm_report.pdf',
        'author': 'RDA',
        'created_date': '2024-10-25'
    }

    # 청킹 수행
    chunks = chunker.chunk(sample_text, metadata)

    print(f"=== Chunking 결과 ===")
    print(f"총 청크 수: {len(chunks)}\n")

    for chunk in chunks:
        print(f"[{chunk['chunk_id']}]")
        print(f"문자 수: {chunk['metadata']['char_count']}")
        print(f"전체 청크: {chunk['metadata']['total_chunks']}")
        print(f"텍스트: {chunk['text'][:100]}...")
        print("-" * 60)
