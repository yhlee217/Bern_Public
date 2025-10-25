"""
02. 로그 파서 예제 (Log Baseline Parser)

정규식 기반의 단순 로그 파싱 예제입니다.
시스템 로그를 파싱하여 타임스탬프, 로그 레벨, 메시지를 추출합니다.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter


class LogBaselineParser:
    """
    단순 정규식 기반 로그 파서

    지원 로그 포맷:
    - [타임스탬프] [레벨] 메시지
    - 타임스탬프 레벨 메시지
    - 레벨: 타임스탬프 - 메시지
    """

    def __init__(self):
        # 여러 로그 포맷 패턴
        self.patterns = [
            # 패턴 1: [2025-10-19 10:30:45] [ERROR] Database connection failed
            re.compile(
                r'\[(?P<timestamp>[\d\-\s:]+)\]\s*'
                r'\[(?P<level>\w+)\]\s*'
                r'(?P<message>.*)'
            ),
            # 패턴 2: 2025-10-19 10:30:45 ERROR Database connection failed
            re.compile(
                r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
                r'(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\s+'
                r'(?P<message>.*)'
            ),
            # 패턴 3: ERROR: 2025-10-19 10:30:45 - Database connection failed
            re.compile(
                r'(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL):\s*'
                r'(?P<timestamp>[\d\-\s:]+)\s*-\s*'
                r'(?P<message>.*)'
            ),
        ]

    def parse(self, log_line: str) -> Optional[Dict]:
        """
        로그 라인 파싱

        Args:
            log_line: 로그 문자열

        Returns:
            파싱 결과 딕셔너리 또는 None (파싱 실패 시)
        """
        for pattern in self.patterns:
            match = pattern.match(log_line.strip())
            if match:
                result = match.groupdict()
                # 타임스탬프 정규화
                result['timestamp'] = result['timestamp'].strip()
                result['level'] = result['level'].upper()
                return result
        return None

    def parse_file(self, filepath: str) -> List[Dict]:
        """
        로그 파일 전체 파싱

        Args:
            filepath: 로그 파일 경로

        Returns:
            파싱된 로그 리스트
        """
        parsed_logs = []
        failed_lines = []

        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                result = self.parse(line)
                if result:
                    result['line_number'] = line_num
                    result['raw'] = line.strip()
                    parsed_logs.append(result)
                else:
                    failed_lines.append((line_num, line.strip()))

        return parsed_logs, failed_lines

    def analyze_logs(self, parsed_logs: List[Dict]) -> Dict:
        """
        로그 분석 통계

        Args:
            parsed_logs: 파싱된 로그 리스트

        Returns:
            분석 결과
        """
        if not parsed_logs:
            return {}

        level_counts = Counter(log['level'] for log in parsed_logs)
        total = len(parsed_logs)

        return {
            'total_logs': total,
            'level_distribution': dict(level_counts),
            'error_count': level_counts.get('ERROR', 0) + level_counts.get('CRITICAL', 0) + level_counts.get('FATAL', 0),
            'warning_count': level_counts.get('WARN', 0) + level_counts.get('WARNING', 0),
            'info_count': level_counts.get('INFO', 0),
            'debug_count': level_counts.get('DEBUG', 0),
        }


class AdvancedLogParser(LogBaselineParser):
    """
    확장된 로그 파서 - IP 주소, 사용자, 경로 등 추출
    """

    def __init__(self):
        super().__init__()
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self.user_pattern = re.compile(r'user[:\s]+(\w+)', re.IGNORECASE)
        self.path_pattern = re.compile(r'(/[\w/.-]+)')

    def extract_metadata(self, message: str) -> Dict:
        """
        메시지에서 메타데이터 추출
        """
        metadata = {}

        # IP 주소 추출
        ip_match = self.ip_pattern.search(message)
        if ip_match:
            metadata['ip_address'] = ip_match.group()

        # 사용자 추출
        user_match = self.user_pattern.search(message)
        if user_match:
            metadata['user'] = user_match.group(1)

        # 파일 경로 추출
        path_match = self.path_pattern.search(message)
        if path_match:
            metadata['path'] = path_match.group()

        return metadata


def demo_basic_parsing():
    """기본 로그 파싱 예제"""
    print("=" * 70)
    print("예제 1: 기본 로그 파싱")
    print("=" * 70)

    parser = LogBaselineParser()

    # 다양한 형식의 로그
    logs = [
        "[2025-10-19 10:30:45] [ERROR] Database connection failed",
        "2025-10-19 10:31:22 INFO User login successful",
        "ERROR: 2025-10-19 10:32:10 - Invalid credentials",
        "[2025-10-19 10:33:05] [WARNING] High memory usage detected",
        "2025-10-19 10:34:18 DEBUG Request processing started",
    ]

    for log in logs:
        result = parser.parse(log)
        if result:
            print(f"\n원본: {log}")
            print(f"  ├─ 타임스탬프: {result['timestamp']}")
            print(f"  ├─ 레벨:       {result['level']}")
            print(f"  └─ 메시지:     {result['message']}")
        else:
            print(f"\n⚠️  파싱 실패: {log}")


def demo_file_parsing():
    """파일에서 로그 읽어서 파싱"""
    print("\n" + "=" * 70)
    print("예제 2: 파일에서 로그 파싱 및 분석")
    print("=" * 70)

    parser = LogBaselineParser()

    try:
        parsed_logs, failed_lines = parser.parse_file('data/sample_logs.txt')

        print(f"\n✅ 성공적으로 파싱된 로그: {len(parsed_logs)}개")
        if failed_lines:
            print(f"⚠️  파싱 실패한 로그: {len(failed_lines)}개")

        # 분석 결과
        stats = parser.analyze_logs(parsed_logs)
        print("\n📊 로그 분석 결과:")
        print(f"  전체 로그 수:  {stats['total_logs']}")
        print(f"  ERROR 로그:    {stats['error_count']}")
        print(f"  WARNING 로그:  {stats['warning_count']}")
        print(f"  INFO 로그:     {stats['info_count']}")
        print(f"  DEBUG 로그:    {stats['debug_count']}")

        print("\n레벨별 분포:")
        for level, count in stats['level_distribution'].items():
            percentage = (count / stats['total_logs']) * 100
            print(f"  {level:10} {count:3}개 ({percentage:5.1f}%)")

        # 샘플 로그 출력
        print("\n📝 샘플 로그 (최대 5개):")
        for log in parsed_logs[:5]:
            print(f"  [{log['level']}] {log['message'][:50]}...")

    except FileNotFoundError:
        print("\n⚠️  data/sample_logs.txt 파일을 찾을 수 없습니다.")
        print("   먼저 테스트 데이터 파일을 생성해주세요.")


def demo_advanced_parsing():
    """고급 메타데이터 추출"""
    print("\n" + "=" * 70)
    print("예제 3: 메타데이터 추출")
    print("=" * 70)

    parser = AdvancedLogParser()

    logs = [
        "[2025-10-19 10:30:45] [ERROR] Connection from 192.168.1.100 failed",
        "[2025-10-19 10:31:22] [INFO] User: admin logged in successfully",
        "[2025-10-19 10:32:10] [ERROR] File not found: /var/log/app.log",
        "[2025-10-19 10:33:05] [WARNING] User: guest attempted access from 10.0.0.50",
    ]

    for log in logs:
        result = parser.parse(log)
        if result:
            metadata = parser.extract_metadata(result['message'])
            print(f"\n원본: {log}")
            print(f"  메시지: {result['message']}")
            if metadata:
                print(f"  메타데이터:")
                for key, value in metadata.items():
                    print(f"    - {key}: {value}")


def demo_error_filtering():
    """에러 로그만 필터링"""
    print("\n" + "=" * 70)
    print("예제 4: 에러 로그 필터링")
    print("=" * 70)

    parser = LogBaselineParser()

    try:
        parsed_logs, _ = parser.parse_file('data/sample_logs.txt')

        # 에러만 필터링
        error_logs = [log for log in parsed_logs
                      if log['level'] in ['ERROR', 'CRITICAL', 'FATAL']]

        print(f"\n🔴 전체 {len(parsed_logs)}개 로그 중 에러 {len(error_logs)}개 발견\n")

        for log in error_logs[:10]:  # 최대 10개
            print(f"[{log['timestamp']}] {log['message']}")

    except FileNotFoundError:
        print("\n⚠️  data/sample_logs.txt 파일을 찾을 수 없습니다.")


if __name__ == "__main__":
    print("\n🔍 로그 파서 (Log Baseline Parser) 예제")
    print("=" * 70)

    # 예제 실행
    demo_basic_parsing()
    demo_file_parsing()
    demo_advanced_parsing()
    demo_error_filtering()

    print("\n" + "=" * 70)
    print("✅ 모든 예제 실행 완료!")
    print("=" * 70)
