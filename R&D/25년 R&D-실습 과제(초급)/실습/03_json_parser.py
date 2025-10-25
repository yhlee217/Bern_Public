"""
03. JSON 파서 예제 (JSON Validation Parser)

데이터 검증용 JSON 파서입니다.
스키마 검증, 데이터 타입 확인, 필수 필드 검사 등을 수행합니다.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class JSONBaselineParser:
    """
    기본 JSON 파서 및 검증기

    기능:
    - JSON 파싱
    - 스키마 검증
    - 데이터 타입 확인
    - 필수 필드 검사
    """

    def __init__(self, schema: Optional[Dict] = None):
        """
        Args:
            schema: 검증할 JSON 스키마 (선택사항)
        """
        self.schema = schema
        self.errors = []

    def parse(self, json_string: str) -> Optional[Dict]:
        """
        JSON 문자열 파싱

        Args:
            json_string: JSON 형식 문자열

        Returns:
            파싱된 딕셔너리 또는 None
        """
        try:
            data = json.loads(json_string)
            self.errors = []
            return data
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON 파싱 오류: {str(e)}")
            return None

    def parse_file(self, filepath: str) -> Optional[Dict]:
        """
        JSON 파일 파싱

        Args:
            filepath: JSON 파일 경로

        Returns:
            파싱된 데이터
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.errors = []
                return data
        except FileNotFoundError:
            self.errors.append(f"파일을 찾을 수 없음: {filepath}")
            return None
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON 파싱 오류: {str(e)}")
            return None

    def validate(self, data: Dict) -> bool:
        """
        스키마 기반 데이터 검증

        Args:
            data: 검증할 데이터

        Returns:
            검증 성공 여부
        """
        if not self.schema:
            return True

        self.errors = []
        return self._validate_recursive(data, self.schema, "root")

    def _validate_recursive(self, data: Any, schema: Dict, path: str) -> bool:
        """재귀적 스키마 검증"""
        is_valid = True

        # 필수 필드 검사
        if 'required' in schema:
            for field in schema['required']:
                if field not in data:
                    self.errors.append(f"{path}: 필수 필드 누락 '{field}'")
                    is_valid = False

        # 필드별 타입 검사
        if 'properties' in schema:
            for field, field_schema in schema['properties'].items():
                if field in data:
                    if not self._validate_type(data[field], field_schema, f"{path}.{field}"):
                        is_valid = False

        return is_valid

    def _validate_type(self, value: Any, schema: Dict, path: str) -> bool:
        """데이터 타입 검증"""
        expected_type = schema.get('type')

        if expected_type == 'string' and not isinstance(value, str):
            self.errors.append(f"{path}: 문자열이 아님 (값: {value})")
            return False
        elif expected_type == 'number' and not isinstance(value, (int, float)):
            self.errors.append(f"{path}: 숫자가 아님 (값: {value})")
            return False
        elif expected_type == 'integer' and not isinstance(value, int):
            self.errors.append(f"{path}: 정수가 아님 (값: {value})")
            return False
        elif expected_type == 'boolean' and not isinstance(value, bool):
            self.errors.append(f"{path}: 불리언이 아님 (값: {value})")
            return False
        elif expected_type == 'array' and not isinstance(value, list):
            self.errors.append(f"{path}: 배열이 아님 (값: {value})")
            return False
        elif expected_type == 'object' and not isinstance(value, dict):
            self.errors.append(f"{path}: 객체가 아님 (값: {value})")
            return False

        # 추가 제약 조건 검사
        if 'minLength' in schema and isinstance(value, str):
            if len(value) < schema['minLength']:
                self.errors.append(f"{path}: 최소 길이 {schema['minLength']} 미만")
                return False

        if 'maxLength' in schema and isinstance(value, str):
            if len(value) > schema['maxLength']:
                self.errors.append(f"{path}: 최대 길이 {schema['maxLength']} 초과")
                return False

        if 'minimum' in schema and isinstance(value, (int, float)):
            if value < schema['minimum']:
                self.errors.append(f"{path}: 최소값 {schema['minimum']} 미만")
                return False

        if 'maximum' in schema and isinstance(value, (int, float)):
            if value > schema['maximum']:
                self.errors.append(f"{path}: 최대값 {schema['maximum']} 초과")
                return False

        return True

    def get_errors(self) -> List[str]:
        """검증 오류 목록 반환"""
        return self.errors


def demo_basic_parsing():
    """기본 JSON 파싱"""
    print("=" * 70)
    print("예제 1: 기본 JSON 파싱")
    print("=" * 70)

    parser = JSONBaselineParser()

    # 정상 JSON
    valid_json = '''
    {
        "name": "홍길동",
        "age": 30,
        "email": "hong@example.com",
        "active": true
    }
    '''

    print("\n✅ 정상 JSON 파싱:")
    data = parser.parse(valid_json)
    if data:
        for key, value in data.items():
            print(f"  {key}: {value} ({type(value).__name__})")

    # 잘못된 JSON
    invalid_json = '''
    {
        "name": "홍길동",
        "age": 30,
        "email": "hong@example.com"  // 주석은 허용되지 않음
    }
    '''

    print("\n❌ 잘못된 JSON 파싱:")
    data = parser.parse(invalid_json)
    if data is None:
        print(f"  오류: {parser.get_errors()}")


def demo_schema_validation():
    """스키마 기반 검증"""
    print("\n" + "=" * 70)
    print("예제 2: 스키마 기반 검증")
    print("=" * 70)

    # 사용자 데이터 스키마 정의
    user_schema = {
        'type': 'object',
        'required': ['name', 'email', 'age'],
        'properties': {
            'name': {
                'type': 'string',
                'minLength': 2,
                'maxLength': 50
            },
            'email': {
                'type': 'string',
                'minLength': 5
            },
            'age': {
                'type': 'integer',
                'minimum': 0,
                'maximum': 150
            },
            'active': {
                'type': 'boolean'
            }
        }
    }

    parser = JSONBaselineParser(schema=user_schema)

    # 정상 데이터
    valid_data = {
        "name": "홍길동",
        "email": "hong@example.com",
        "age": 30,
        "active": True
    }

    print("\n✅ 정상 데이터 검증:")
    if parser.validate(valid_data):
        print("  검증 성공!")
    else:
        print(f"  검증 실패: {parser.get_errors()}")

    # 비정상 데이터 1: 필수 필드 누락
    invalid_data1 = {
        "name": "홍길동",
        "age": 30
        # email 필드 누락
    }

    print("\n❌ 필수 필드 누락:")
    if parser.validate(invalid_data1):
        print("  검증 성공!")
    else:
        print("  검증 실패:")
        for error in parser.get_errors():
            print(f"    - {error}")

    # 비정상 데이터 2: 타입 불일치
    invalid_data2 = {
        "name": "홍길동",
        "email": "hong@example.com",
        "age": "30세",  # 문자열이지만 정수여야 함
        "active": True
    }

    print("\n❌ 타입 불일치:")
    if parser.validate(invalid_data2):
        print("  검증 성공!")
    else:
        print("  검증 실패:")
        for error in parser.get_errors():
            print(f"    - {error}")

    # 비정상 데이터 3: 값 범위 초과
    invalid_data3 = {
        "name": "홍",  # 너무 짧음
        "email": "hong@example.com",
        "age": 200,  # 최대값 초과
        "active": True
    }

    print("\n❌ 값 범위 초과:")
    if parser.validate(invalid_data3):
        print("  검증 성공!")
    else:
        print("  검증 실패:")
        for error in parser.get_errors():
            print(f"    - {error}")


def demo_file_parsing():
    """파일에서 JSON 읽기"""
    print("\n" + "=" * 70)
    print("예제 3: 파일에서 JSON 파싱")
    print("=" * 70)

    parser = JSONBaselineParser()

    try:
        data = parser.parse_file('data/sample_data.json')

        if data:
            print("\n✅ 파일 파싱 성공!")
            print(f"\n데이터 구조:")

            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  {key}: 배열 (크기: {len(value)})")
                    elif isinstance(value, dict):
                        print(f"  {key}: 객체 (키: {len(value)}개)")
                    else:
                        print(f"  {key}: {value}")

            # 샘플 데이터 출력
            print(f"\n전체 데이터 (Pretty Print):")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")

        else:
            print(f"\n❌ 파일 파싱 실패: {parser.get_errors()}")

    except Exception as e:
        print(f"\n⚠️  오류 발생: {str(e)}")


def demo_batch_validation():
    """여러 데이터 일괄 검증"""
    print("\n" + "=" * 70)
    print("예제 4: 여러 데이터 일괄 검증")
    print("=" * 70)

    # 제품 스키마
    product_schema = {
        'type': 'object',
        'required': ['id', 'name', 'price'],
        'properties': {
            'id': {'type': 'integer', 'minimum': 1},
            'name': {'type': 'string', 'minLength': 1},
            'price': {'type': 'number', 'minimum': 0},
            'stock': {'type': 'integer', 'minimum': 0}
        }
    }

    parser = JSONBaselineParser(schema=product_schema)

    products = [
        {"id": 1, "name": "노트북", "price": 1500000, "stock": 10},
        {"id": 2, "name": "마우스", "price": 30000, "stock": 50},
        {"id": 3, "name": "키보드", "price": -5000, "stock": 20},  # 가격 음수
        {"id": 4, "name": "", "price": 80000, "stock": 15},  # 이름 비어있음
        {"id": 5, "price": 200000, "stock": 5},  # ID 누락... 아니 name 누락
    ]

    print(f"\n총 {len(products)}개 제품 검증 중...\n")

    valid_count = 0
    invalid_count = 0

    for i, product in enumerate(products, 1):
        if parser.validate(product):
            print(f"✅ 제품 {i}: {product.get('name', 'N/A')} - 검증 성공")
            valid_count += 1
        else:
            print(f"❌ 제품 {i}: 검증 실패")
            for error in parser.get_errors():
                print(f"     - {error}")
            invalid_count += 1

    print(f"\n📊 검증 결과: 성공 {valid_count}개 / 실패 {invalid_count}개")


if __name__ == "__main__":
    print("\n📋 JSON 파서 및 검증기 예제")
    print("=" * 70)

    # 예제 실행
    demo_basic_parsing()
    demo_schema_validation()
    demo_file_parsing()
    demo_batch_validation()

    print("\n" + "=" * 70)
    print("✅ 모든 예제 실행 완료!")
    print("=" * 70)
