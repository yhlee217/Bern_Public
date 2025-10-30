"""
[*] TXT [*] [*] [*]

[*] [*] [*] [*] [*] [*] [*] [*] [*] [*].

[*] [*]:
1. [*] [*] [*] [*] [*] [*]
2. [*] [*] [*] [*]
3. [*] [*] [*] [*] [*]
"""

import os
import time
from typing import Generator, List
import random
import string


class LargeFileParser:
    """
    [*] [*] [*] [*] [*] [*] [*]
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): [*] [*] [*]
        """
        self.file_path = file_path
        self.file_size = None

        # [*] [*] [*] [*] [*]
        if os.path.exists(file_path):
            self.file_size = os.path.getsize(file_path)
            print(f"[*] [*] [*]: {self._format_size(self.file_size)}")

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """
        [*] [*] [*] [*] [*] [*] [*]

        Args:
            size_bytes (int): [*] [*] [*]

        Returns:
            str: [*] [*] [*] ([*]: '1.5 MB')
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def read_lines_generator(self) -> Generator[str, None, None]:
        """
        [*] [*] [*] [*] [*] [*] ([*] [*])

        Yields:
            str: [*] [*] [*] ([*] [*] [*])

        [*]:
            - [*] [*] [*] [*] [*]
            - [*] [*] [*] [*]
            - [*] [*] [*] [*]
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # [*] [*] [*] [*]
                    yield line.strip()

        except Exception as e:
            print(f"[ERROR] [*] [*] [*]: {e}")

    def read_in_chunks(self, chunk_size: int = 1000) -> Generator[List[str], None, None]:
        """
        [*] [*]([*]) [*] [*]

        Args:
            chunk_size (int): [*] [*] [*] [*] [*]

        Yields:
            List[str]: chunk_size [*] [*] [*] [*]

        [*] [*]:
            - [*] [*] [*] [*]
            - [*] [*] [*] [*] [*]
            - [*] [*] [*] [*] [*]
        """
        chunk = []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    chunk.append(line.strip())

                    # [*] [*] [*] yield
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []  # [*] [*]

                # [*] [*] [*] [*]
                if chunk:
                    yield chunk

        except Exception as e:
            print(f"[ERROR] [*] [*] [*]: {e}")

    def count_lines(self) -> int:
        """
        [*] [*] [*] [*] [*] ([*] [*])

        Returns:
            int: [*] [*] [*]

        Note:
            - [*] [*] [*] [*] [*]
            - [*] [*] [*] [*] [*]
        """
        count = 0

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                # sum[*] [*] [*] [*] [*] [*]
                count = sum(1 for _ in f)

            print(f"[STATS] [*] [*] [*]: {count:,}[*]")
            return count

        except Exception as e:
            print(f"[ERROR] [*] [*] [*]: {e}")
            return 0

    def filter_lines(self, condition) -> Generator[str, None, None]:
        """
        [*] [*] [*] [*] [*]

        Args:
            condition (callable): [*] [*] [*]
                [*]: lambda line: 'ERROR' in line

        Yields:
            str: [*] [*] [*]

        [*]:
            - [*] [*] [*] [*] [*]
            - [*] [*] [*] [*]
        """
        matched_count = 0

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()

                    if condition(line):
                        matched_count += 1
                        yield line

            print(f"[SEARCH] [*] [*]: {matched_count:,}[*] [*]")

        except Exception as e:
            print(f"[ERROR] [*] [*]: {e}")

    def get_sample_lines(self, n: int = 10) -> List[str]:
        """
        [*] n[*] [*] [*] [*]

        Args:
            n (int): [*] [*] [*]

        Returns:
            List[str]: [*] [*] [*]

        [*]:
            - [*] [*] [*]
            - [*] [*] [*]
            - [*]
        """
        samples = []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= n:
                        break
                    samples.append(line.strip())

            print(f"[INFO] {len(samples)}[*] [*] [*] [*]")
            return samples

        except Exception as e:
            print(f"[ERROR] [*] [*] [*]: {e}")
            return []

    def search_pattern(self, pattern: str, case_sensitive: bool = False) -> List[dict]:
        """
        [*] [*] [*] [*]

        Args:
            pattern (str): [*] [*]
            case_sensitive (bool): [*] [*] [*]

        Returns:
            List[dict]: [*] [*] [*]
                [
                    {'line_number': 10, 'content': '...'},
                    ...
                ]
        """
        matches = []

        # [*] [*] [*]
        search_pattern = pattern if case_sensitive else pattern.lower()

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    line_stripped = line.strip()

                    # [*] [*] [*]
                    search_target = line_stripped if case_sensitive else line_stripped.lower()

                    # [*] [*]
                    if search_pattern in search_target:
                        matches.append({
                            'line_number': line_num,
                            'content': line_stripped
                        })

            print(f"[FIND] '{pattern}' [*] [*]: {len(matches):,}[*] [*]")
            return matches

        except Exception as e:
            print(f"[ERROR] [*] [*]: {e}")
            return []


class LargeFileGenerator:
    """
    [*] [*] [*] [*] [*]
    """

    @staticmethod
    def generate_random_line(line_num: int) -> str:
        """
        [*] [*] [*] [*]

        Args:
            line_num (int): [*] [*]

        Returns:
            str: [*] [*] [*]
        """
        # [*] [*]
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        # [*] [*] [*]
        levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
        level = random.choice(levels)

        # [*] [*]
        messages = [
            "Application started successfully",
            "Database connection established",
            "Processing user request",
            "Cache updated",
            "Task completed",
            "Connection timeout occurred",
            "Invalid input received",
            "Memory usage: {}MB".format(random.randint(100, 2000)),
            "CPU usage: {}%".format(random.randint(10, 90)),
            "Request processed in {}ms".format(random.randint(10, 500))
        ]
        message = random.choice(messages)

        return f"2025-10-23 {hour:02d}:{minute:02d}:{second:02d} [{level}] {message}"

    @staticmethod
    def create_large_file(file_path: str, num_lines: int = 100000):
        """
        [*] [*] [*] [*]

        Args:
            file_path (str): [*] [*] [*]
            num_lines (int): [*] [*] [*]

        Note:
            - 10[*] [*] ≈ 10-15MB
            - 100[*] [*] ≈ 100-150MB
            - 1000[*] [*] ≈ 1-1.5GB
        """
        print(f"[INFO] [*] [*] [*] [*]: {num_lines:,}[*]...")

        start_time = time.time()

        try:
            # [*] [*]
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                for i in range(1, num_lines + 1):
                    line = LargeFileGenerator.generate_random_line(i)
                    f.write(line + '\n')

                    # [*] [*] [*] (10% [*])
                    if i % (num_lines // 10) == 0:
                        progress = (i / num_lines) * 100
                        print(f"  [*]: {progress:.0f}% ({i:,}/{num_lines:,}[*])")

            elapsed = time.time() - start_time
            file_size = os.path.getsize(file_path)

            print(f"[OK] [*] [*] [*]!")
            print(f"   - [*]: {file_path}")
            print(f"   - [*]: {LargeFileParser._format_size(file_size)}")
            print(f"   - [*] [*]: {elapsed:.2f}[*]")

        except Exception as e:
            print(f"[ERROR] [*] [*] [*]: {e}")


def benchmark_methods(file_path: str):
    """
    [*] [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*]
    """
    print("\n" + "=" * 60)
    print("[TIMER]  [*] [*]")
    print("=" * 60)

    # [*] 1: readlines() ([*])
    print("\n1.  [*] 1: readlines() - [*] [*] [*]")
    start = time.time()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            count = len(lines)
    except MemoryError:
        print("  [ERROR] [*] [*]!")
        count = 0
    elapsed1 = time.time() - start
    print(f"  [*]: {count:,}[*] / [*] [*]: {elapsed1:.3f}[*]")

    # [*] 2: [*] ([*])
    print("\n2.  [*] 2: [*] - [*] [*] [*]")
    start = time.time()
    parser = LargeFileParser(file_path)
    count = sum(1 for _ in parser.read_lines_generator())
    elapsed2 = time.time() - start
    print(f"  [*]: {count:,}[*] / [*] [*]: {elapsed2:.3f}[*]")

    # [*] 3: sum + [*] [*] ([*] [*])
    print("\n3.  [*] 3: sum + [*] [*]")
    start = time.time()
    count = parser.count_lines()
    elapsed3 = time.time() - start
    print(f"  [*] [*]: {elapsed3:.3f}[*]")

    # [*] [*]
    print("\n[STATS] [*] [*]:")
    if elapsed1 > 0:
        print(f"  - [*] 2[*] [*] 1[*] {elapsed1/elapsed2:.2f}[*] [*]")
        print(f"  - [*] 3[*] [*] 1[*] {elapsed1/elapsed3:.2f}[*] [*]")


def main():
    """
    [*] [*]: [*] [*] [*] [*]
    """
    print("=" * 60)
    print("[*] TXT [*] [*] [*]")
    print("=" * 60)

    large_file = "data/large_log_file.txt"

    # [*] [*] [*] [*] (10[*] [*])
    if not os.path.exists(large_file):
        print("\n[INFO] [*] [*] [*] [*]...")
        print("([*] [*] [*] [*] [*])\n")

        # 10[*] [*] [*] ([*] 10-15MB)
        LargeFileGenerator.create_large_file(large_file, num_lines=100000)

    # [*] [*]
    parser = LargeFileParser(large_file)

    # 1. [*] [*] [*]
    print("\n" + "=" * 60)
    print("1. [*] [*] [*] [*]")
    print("=" * 60)
    parser.count_lines()

    # 2. [*] [*] [*]
    print("\n" + "=" * 60)
    print("2. [*] [*] [*] ([*] 5[*])")
    print("=" * 60)
    samples = parser.get_sample_lines(5)
    for i, line in enumerate(samples, 1):
        print(f"  {i}. {line}")

    # 3. [*] [*] [*]
    print("\n" + "=" * 60)
    print("3. ERROR [*] [*]")
    print("=" * 60)
    error_filter = lambda line: 'ERROR' in line
    error_count = 0

    print("ERROR [*] [*] ([*] 5[*]):")
    for i, line in enumerate(parser.filter_lines(error_filter), 1):
        error_count += 1
        if i <= 5:
            print(f"  {i}. {line}")
        if i > 5:
            break

    # 4. [*] [*]
    print("\n" + "=" * 60)
    print("4. 'Database' [*] [*]")
    print("=" * 60)
    matches = parser.search_pattern('Database', case_sensitive=False)

    if matches:
        print(f"\n[*] [*] [*] ([*] 3[*]):")
        for match in matches[:3]:
            print(f"  [*] {match['line_number']}: {match['content']}")

    # 5. [*] [*] [*]
    print("\n" + "=" * 60)
    print("5. [*] [*] [*] (10,000[*])")
    print("=" * 60)

    chunk_count = 0
    total_lines = 0

    for chunk in parser.read_in_chunks(chunk_size=10000):
        chunk_count += 1
        total_lines += len(chunk)
        print(f"  [*] {chunk_count}: {len(chunk):,}[*] [*] ([*]: {total_lines:,}[*])")

    # 6. [*] [*]
    benchmark_methods(large_file)

    print("\n" + "=" * 60)
    print("[*] [*]!")
    print("=" * 60)

    print("\n[TIP] [*] [*] [*]:")
    print("  1. [*] [*] [*] [*] (multiprocessing)")
    print("  2. [*] [*] [*] (memory_profiler)")
    print("  3. [*] [*] [*] [*] [*]")
    print("  4. [*] [*] [*] [*]")


if __name__ == "__main__":
    main()
