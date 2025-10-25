"""
실습: Elasticsearch 기본 작업 (Mock)
"""
import sys, io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class MockElasticsearch:
    """Elasticsearch Mock 클래스"""

    def __init__(self):
        self.docs = {}

    def index(self, index, id, document):
        """문서 저장"""
        if index not in self.docs:
            self.docs[index] = {}
        self.docs[index][id] = document
        return {'result': 'created', '_id': id}

    def get(self, index, id):
        """문서 조회"""
        if index in self.docs and id in self.docs[index]:
            return {'_source': self.docs[index][id]}
        return None

    def search(self, index, body):
        """검색"""
        query_text = body.get('query', {}).get('match', {}).get('content', '')

        results = []
        if index in self.docs:
            for doc_id, doc in self.docs[index].items():
                if query_text.lower() in doc.get('content', '').lower():
                    results.append({
                        '_id': doc_id,
                        '_score': 1.0,
                        '_source': doc
                    })

        return {'hits': {'hits': results, 'total': {'value': len(results)}}}

if __name__ == '__main__':
    # Mock Elasticsearch
    es = MockElasticsearch()

    print("=== Elasticsearch 기본 작업 (Mock) ===\n")

    # 1. 문서 저장
    doc = {
        'title': '스마트팜 기술',
        'content': 'ICT 기술을 활용한 농업 시스템'
    }

    result = es.index(index='docs', id='1', document=doc)
    print(f"1. 저장: {result['result']}\n")

    # 2. 문서 조회
    retrieved = es.get(index='docs', id='1')
    print(f"2. 조회: {retrieved['_source']}\n")

    # 3. 검색
    search_result = es.search(
        index='docs',
        body={'query': {'match': {'content': 'ICT'}}}
    )

    print(f"3. 검색 결과: {search_result['hits']['total']['value']}개")
    for hit in search_result['hits']['hits']:
        print(f"   - {hit['_source']['title']}")

    print("\n실제 사용 시 Elasticsearch 서버 필요!")
    print("설치: docker run -p 9200:9200 elasticsearch:8.11.0")
