"""
[*] [*] [*] [*]

[*] [*] [*] [*] [*] [*] [*] [*] [*] [*].

[*] [*]:
1. [*](Regular Expression) [*] [*]
2. [*] [*] [*] [*] [*] [*]
3. [*] [*] [*] [*] [*]
"""

import re
import os
from datetime import datetime
from collections import Counter


class LogParser:
    """
    [*] [*] [*] [*]

    [*] [*] [*]:
        [[*]] [[*]] [[*]] [*]
        [*]: 2025-10-23 14:30:45 [ERROR] Database connection failed
    """

    def __init__(self):
        """
        [*] [*] [*]

        [*] [*] [*]:
            (?P<date>\\d{4}-\\d{2}-\\d{2})  : [*] (YYYY-MM-DD)
            (?P<time>\\d{2}:\\d{2}:\\d{2})  : [*] (HH:MM:SS)
            (?P<level>\\w+)                 : [*] [*] (INFO, ERROR [*])
            (?P<message>.*)                 : [*] [*] ([*] [*])
        """
        # [*] [*] [*] (named group [*])
        self.pattern = re.compile(
            r'(?P<date>\d{4}-\d{2}-\d{2})\s+'  # [*]
            r'(?P<time>\d{2}:\d{2}:\d{2})\s+'  # [*]
            r'\[(?P<level>\w+)\]\s+'            # [*] [*] ([*] [*])
            r'(?P<message>.*)'                  # [*]
        )

        # [*] [*]
        self.total_lines = 0      # [*] [*] [*]
        self.parsed_lines = 0     # [*] [*] [*] [*]
        self.failed_lines = 0     # [*] [*] [*] [*]

    def parse_line(self, line):
        """
        [*] [*] [*] [*]

        Args:
            line (str): [*] [*]

        Returns:
            dict or None: [*] [*] [*] [*], [*] [*] None

        [*] [*] [*]:
            {
                'date': '2025-10-23',
                'time': '14:30:45',
                'level': 'ERROR',
                'message': 'Database connection failed',
                'timestamp': datetime [*]
            }
        """
        # [*] [*]
        match = self.pattern.match(line.strip())

        if match:
            # named group[*] [*] [*]
            result = match.groupdict()

            # [*] [*] datetime [*] [*]
            try:
                result['timestamp'] = datetime.strptime(
                    f"{result['date']} {result['time']}",
                    "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                # [*] [*] [*] [*]
                result['timestamp'] = None

            return result

        return None

    def parse_file(self, file_path):
        """
        [*] [*] [*] [*]

        Args:
            file_path (str): [*] [*] [*]

        Returns:
            list: [*] [*] [*] [*]
        """
        logs = []
        self.total_lines = 0
        self.parsed_lines = 0
        self.failed_lines = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    self.total_lines += 1

                    # [*] [*] [*]
                    if not line.strip():
                        continue

                    # [*] [*]
                    parsed = self.parse_line(line)

                    if parsed:
                        # [*] [*] [*]
                        parsed['line_number'] = line_num
                        parsed['raw_line'] = line.strip()
                        logs.append(parsed)
                        self.parsed_lines += 1
                    else:
                        # [*] [*]
                        self.failed_lines += 1
                        print(f"[WARN]  [*] [*] ([*] {line_num}): {line.strip()[:50]}...")

            print(f"\n[OK] [*] [*]:")
            print(f"   - [*] [*]: {self.total_lines}")
            print(f"   - [*]: {self.parsed_lines}")
            print(f"   - [*]: {self.failed_lines}")

            return logs

        except FileNotFoundError:
            print(f"[ERROR] [*] [*] [*] [*]: {file_path}")
            return []
        except Exception as e:
            print(f"[ERROR] [*] [*] [*]: {e}")
            return []

    def filter_by_level(self, logs, level):
        """
        [*] [*] [*] [*]

        Args:
            logs (list): [*] [*] [*]
            level (str): [*] [*] [*] ([*]: 'ERROR', 'INFO')

        Returns:
            list: [*] [*] [*]
        """
        filtered = [log for log in logs if log['level'] == level]
        print(f"\n[SEARCH] '{level}' [*] [*]: {len(filtered)}[*]")
        return filtered

    def filter_by_date_range(self, logs, start_date, end_date):
        """
        [*] [*] [*] [*]

        Args:
            logs (list): [*] [*] [*]
            start_date (str): [*] [*] (YYYY-MM-DD)
            end_date (str): [*] [*] (YYYY-MM-DD)

        Returns:
            list: [*] [*] [*]
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        filtered = [
            log for log in logs
            if log['timestamp'] and start <= log['timestamp'] <= end
        ]

        print(f"\n[DATE] [*] [*] ({start_date} ~ {end_date}): {len(filtered)}[*]")
        return filtered

    def search_keyword(self, logs, keyword):
        """
        [*] [*] [*]

        Args:
            logs (list): [*] [*] [*]
            keyword (str): [*] [*]

        Returns:
            list: [*] [*] [*] [*]
        """
        # [*] [*] [*] [*]
        keyword_lower = keyword.lower()

        filtered = [
            log for log in logs
            if keyword_lower in log['message'].lower()
        ]

        print(f"\n[FIND] '{keyword}' [*] [*] [*]: {len(filtered)}[*]")
        return filtered

    def get_statistics(self, logs):
        """
        [*] [*] [*]

        Args:
            logs (list): [*] [*] [*]

        Returns:
            dict: [*] [*]
        """
        # [*] [*] [*]
        level_counter = Counter(log['level'] for log in logs)

        # [*] [*]
        date_counter = Counter(log['date'] for log in logs)

        # [*] [*] ([*] [*])
        hour_counter = Counter(
            log['time'].split(':')[0] for log in logs if log['time']
        )

        stats = {
            'total': len(logs),
            'by_level': dict(level_counter),
            'by_date': dict(date_counter),
            'by_hour': dict(sorted(hour_counter.items()))
        }

        return stats

    def print_statistics(self, stats):
        """
        [*] [*] [*] [*] [*]

        Args:
            stats (dict): get_statistics()[*] [*] [*]
        """
        print("\n" + "=" * 60)
        print("[STATS] [*] [*] [*]")
        print("=" * 60)

        print(f"\n[*] [*] [*]: {stats['total']:,}[*]")

        # [*] [*]
        print("\n[>] [*] [*] [*]:")
        for level, count in sorted(stats['by_level'].items()):
            percentage = (count / stats['total']) * 100
            print(f"  {level:10s}: {count:6,}[*] ({percentage:5.1f}%)")

        # [*] [*]
        print("\n[>] [*] [*] [*]:")
        for date, count in sorted(stats['by_date'].items()):
            print(f"  {date}: {count:,}[*]")

        # [*] [*] ([*] 5[*])
        print("\n[>] [*] [*] [*] [*] [*] (Top 5):")
        top_hours = sorted(
            stats['by_hour'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        for hour, count in top_hours:
            print(f"  {hour}[*]: {count:,}[*]")


def create_sample_log_file(file_path):
    """
    [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*]
    """
    sample_logs = """2025-10-23 09:00:15 [INFO] Application started successfully
2025-10-23 09:00:16 [INFO] Loading configuration from config.ini
2025-10-23 09:00:17 [DEBUG] Configuration loaded: database.host=localhost
2025-10-23 09:00:18 [INFO] Connecting to database...
2025-10-23 09:00:20 [ERROR] Database connection failed: Connection timeout
2025-10-23 09:00:21 [WARNING] Retrying database connection (attempt 1/3)
2025-10-23 09:00:23 [INFO] Database connection established
2025-10-23 09:00:24 [INFO] Starting worker threads
2025-10-23 09:00:25 [DEBUG] Worker thread #1 started
2025-10-23 09:00:25 [DEBUG] Worker thread #2 started
2025-10-23 09:00:30 [INFO] Processing request: GET /api/users
2025-10-23 09:00:31 [DEBUG] Query execution time: 0.025s
2025-10-23 09:00:31 [INFO] Request completed: 200 OK
2025-10-23 09:05:42 [ERROR] Unexpected error in worker thread #2
2025-10-23 09:05:42 [ERROR] Stack trace: NullPointerException at line 234
2025-10-23 09:05:43 [WARNING] Worker thread #2 terminated unexpectedly
2025-10-23 09:05:44 [INFO] Restarting worker thread #2
2025-10-23 09:10:15 [INFO] Processing request: POST /api/orders
2025-10-23 09:10:16 [WARNING] Request payload size exceeds limit: 5.2MB
2025-10-23 09:10:17 [ERROR] Request rejected: Payload too large
2025-10-23 10:00:00 [INFO] Hourly health check completed
2025-10-23 10:00:01 [DEBUG] Memory usage: 1.2GB / 4.0GB
2025-10-23 10:00:01 [DEBUG] CPU usage: 35%
2025-10-23 11:30:22 [CRITICAL] Out of memory error detected
2025-10-23 11:30:23 [CRITICAL] Initiating emergency shutdown
2025-10-23 11:30:24 [INFO] Application terminated
"""

    # [*] [*] [*]
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_logs)

    print(f"[OK] [*] [*] [*] [*]: {file_path}")


def main():
    """
    [*] [*]: [*] [*] [*] [*]
    """
    print("=" * 60)
    print("[*] [*] [*] [*]")
    print("=" * 60)

    # [*] [*] [*] [*]
    log_file = "data/sample_application.log"

    # [*] [*] [*] [*]
    if not os.path.exists(log_file):
        print("\n[INFO] [*] [*] [*] [*]...\n")
        create_sample_log_file(log_file)

    # 1. [*] [*] [*]
    parser = LogParser()

    # 2. [*] [*] [*]
    print("\n" + "=" * 60)
    print("1. [*] [*] [*]")
    print("=" * 60)
    logs = parser.parse_file(log_file)

    # 3. [*] [*]
    print("\n" + "=" * 60)
    print("2. [*] [*]")
    print("=" * 60)
    stats = parser.get_statistics(logs)
    parser.print_statistics(stats)

    # 4. [*] [*] [*]
    print("\n" + "=" * 60)
    print("3. ERROR [*] [*] [*]")
    print("=" * 60)
    error_logs = parser.filter_by_level(logs, 'ERROR')

    if error_logs:
        print("\n[*] [*] [*]:")
        for log in error_logs[:5]:  # [*] 5[*] [*]
            print(f"\n  [{log['timestamp']}] {log['level']}")
            print(f"  [*]: {log['message']}")

    # 5. [*] [*]
    print("\n" + "=" * 60)
    print("4. [*] [*] ('database')")
    print("=" * 60)
    db_logs = parser.search_keyword(logs, 'database')

    if db_logs:
        print("\n[*] [*]:")
        for log in db_logs[:3]:  # [*] 3[*] [*]
            print(f"  [{log['time']}] {log['message']}")

    # 6. CRITICAL [*] [*] [*]
    print("\n" + "=" * 60)
    print("5. CRITICAL [*] [*] [*]")
    print("=" * 60)
    critical_logs = parser.filter_by_level(logs, 'CRITICAL')

    if critical_logs:
        print("\n[WARN]  [*] [*] [*]!")
        for log in critical_logs:
            print(f"  [{log['timestamp']}] {log['message']}")
    else:
        print("\n[OK] [*] [*] [*].")

    print("\n" + "=" * 60)
    print("[*] [*]!")
    print("=" * 60)

    # [*] [*] [*]
    print("\n[TIP] [*] [*] [*]:")
    print("  1. [*] CSV [*] [*]")
    print("  2. [*] [*] [*] [*] [*] (matplotlib)")
    print("  3. [*] [*] [*] (tail -f [*])")
    print("  4. [*] [*] [*] [*] [*]")


if __name__ == "__main__":
    main()
