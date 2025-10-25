"""
[*] TXT [*] [*] [*]

[*] [*] TXT [*] [*] [*] [*] [*] [*] [*] [*].

[*] [*]:
1. [*] [*] [*] [*] [*]
2. [*] [*] [*] [*]
3. [*] [*] [*] [*] [*] [*]
"""

import os
import chardet


def read_entire_file(file_path):
    """
    [*] [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*]

    Returns:
        str: [*] [*] [*]

    [*]:
        - [*] [*] [*] [*] [*] [*] [*] [*]
        - [*] [*] [*] [*]
    """
    try:
        # with [*] [*] [*] [*] [*] ([*] [*])
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"[OK] [*] [*] [*]: {len(content)}[*] [*]")
        return content

    except FileNotFoundError:
        print(f"[ERROR] [*]: '{file_path}' [*] [*] [*] [*].")
        return None
    except UnicodeDecodeError:
        print("[ERROR] [*]: UTF-8 [*] [*] [*] [*].")
        return None


def read_lines_as_list(file_path):
    """
    [*] [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*]

    Returns:
        list: [*] [*] [*] [*] [*]

    [*]:
        - readlines()[*] [*] [*](\\n)[*] [*]
        - strip()[*] [*] [*] [*] [*] [*]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # readlines()[*] [*] [*] [*] [*]
            lines = f.readlines()

        # [*] [*] [*] [*] [*] [*]
        lines = [line.strip() for line in lines]

        print(f"[OK] {len(lines)}[*] [*] [*].")
        return lines

    except Exception as e:
        print(f"[ERROR] [*] [*]: {e}")
        return None


def read_lines_one_by_one(file_path):
    """
    [*] [*] [*] [*] [*] ([*] [*])

    Args:
        file_path (str): [*] [*] [*]

    [*]:
        - [*] [*] [*] [*]
        - [*] [*] [*] [*]
        - [*] [*] [*] [*] [*] [*]
    """
    try:
        print("[*] [*] [*] [*] [*]...")
        line_count = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            # for [*] [*] [*] [*] [*] ([*])
            for line in f:
                line_count += 1
                # strip()[*] [*] [*] [*]
                line = line.strip()

                # [*] [*] [*] [*] [*]
                if line:
                    print(f"  [*] {line_count}: {line[:50]}...")  # [*] 50[*] [*]

        print(f"[OK] [*] {line_count}[*] [*] [*].")

    except Exception as e:
        print(f"[ERROR] [*] [*]: {e}")


def detect_file_encoding(file_path):
    """
    [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*] [*]

    Returns:
        str: [*] [*] ([*]: 'utf-8', 'cp949', 'euc-kr')

    [*] [*]:
        - [*] [*] UTF-8, CP949, EUC-KR [*] [*] [*] [*]
        - [*] [*] [*] UnicodeDecodeError [*]
        - chardet [*] [*] [*] [*]
    """
    try:
        # [*] [*]('rb')[*] [*] [*] [*] [*] [*]
        with open(file_path, 'rb') as f:
            # [*] [*] [*] [*] [*] ([*] [*] [*] [*] [*])
            raw_data = f.read(10000)  # [*] 10KB[*] [*]
            result = chardet.detect(raw_data)

        encoding = result['encoding']
        confidence = result['confidence']

        print(f"[INFO] [*] [*]: {encoding} ([*]: {confidence:.2%})")
        return encoding

    except Exception as e:
        print(f"[ERROR] [*] [*] [*]: {e}")
        return 'utf-8'  # [*] UTF-8 [*]


def read_with_auto_encoding(file_path):
    """
    [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*]

    Returns:
        str: [*] [*]

    [*]:
        - [*] [*] [*] [*] [*]
        - UnicodeDecodeError [*] [*] [*]
    """
    # 1[*]: [*] [*]
    encoding = detect_file_encoding(file_path)

    # 2[*]: [*] [*] [*] [*]
    try:
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()

        print(f"[OK] [*] [*] [*] ({encoding} [*] [*])")
        return content

    except Exception as e:
        print(f"[ERROR] [*] [*] [*]: {e}")
        return None


def filter_lines_by_keyword(file_path, keyword):
    """
    [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*]
        keyword (str): [*] [*]

    Returns:
        list: [*] [*] [*] [*]

    [*] [*]:
        - [*] [*] 'ERROR'[*] [*] [*] [*]
        - [*] [*] [*] [*]
    """
    filtered_lines = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                # [*] [*] [*]
                if keyword in line:
                    # [*] [*] [*] [*]
                    filtered_lines.append({
                        'line_number': line_num,
                        'content': line.strip()
                    })

        print(f"[SEARCH] '{keyword}' [*] [*] [*]: {len(filtered_lines)}[*]")
        return filtered_lines

    except Exception as e:
        print(f"[ERROR] [*] [*]: {e}")
        return []


def count_word_frequency(file_path):
    """
    [*] [*] [*] [*] [*]

    Args:
        file_path (str): [*] [*] [*]

    Returns:
        dict: {[*]: [*]} [*]

    [*]:
        - [*] [*]
        - [*] [*]
        - [*] [*]
    """
    word_freq = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # [*] [*] [*] [*]
                words = line.lower().split()

                for word in words:
                    # [*] [*] ([*] [*])
                    word = word.strip('.,!?;:"()[]{}')

                    if word:  # [*] [*] [*] [*]
                        word_freq[word] = word_freq.get(word, 0) + 1

        # [*] [*] [*] ([*] 10[*])
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

        print("\n[STATS] [*] 10[*] [*]:")
        for word, freq in top_words:
            print(f"  {word}: {freq}[*]")

        return word_freq

    except Exception as e:
        print(f"[ERROR] [*] [*] [*] [*]: {e}")
        return {}


def main():
    """
    [*] [*]: [*] [*] [*] [*]
    """
    print("=" * 60)
    print("TXT [*] [*] [*] [*]")
    print("=" * 60)

    # [*] [*] [*] ([*] [*] [*] [*])
    sample_file = "data/sample_text.txt"

    # [*] [*] [*] [*] [*] [*]
    if not os.path.exists(sample_file):
        print("\n[INFO] [*] [*] [*] [*]...")
        os.makedirs(os.path.dirname(sample_file), exist_ok=True)

        sample_content = """[*]. [*] [*] [*] [*].
[*] [*] [*] [*] [*] [*] [*].

[*] [*] [*]:
- [*] [*] [*] [*]
- [*] [*]
- [*] [*]
- [*] [*] [*]

ERROR: [*] [*] [*].
WARNING: [*] [*] [*].
INFO: [*] [*].

[*] [*] [*] [*] [*].
[*] [*] [*] [*].
"""
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)

        print(f"[OK] [*] [*] [*]: {sample_file}")

    # 1. [*] [*] [*]
    print("\n" + "=" * 60)
    print("1. [*] [*] [*] [*] [*]")
    print("=" * 60)
    content = read_entire_file(sample_file)
    if content:
        print(f"[*] [*]:\n{content[:100]}...\n")

    # 2. [*] [*] [*] [*]
    print("\n" + "=" * 60)
    print("2. [*] [*] [*] [*]")
    print("=" * 60)
    lines = read_lines_as_list(sample_file)
    if lines:
        print(f"[*] 3[*]:\n" + "\n".join(lines[:3]))

    # 3. [*] [*] [*] [*]
    print("\n" + "=" * 60)
    print("3. [*] [*] [*] [*] ([*] [*])")
    print("=" * 60)
    read_lines_one_by_one(sample_file)

    # 4. [*] [*] [*]
    print("\n" + "=" * 60)
    print("4. [*] [*] [*]")
    print("=" * 60)
    content = read_with_auto_encoding(sample_file)

    # 5. [*] [*]
    print("\n" + "=" * 60)
    print("5. [*] [*] (ERROR [*])")
    print("=" * 60)
    error_lines = filter_lines_by_keyword(sample_file, "ERROR")
    for item in error_lines:
        print(f"  [*] {item['line_number']}: {item['content']}")

    # 6. [*] [*] [*]
    print("\n" + "=" * 60)
    print("6. [*] [*] [*]")
    print("=" * 60)
    word_freq = count_word_frequency(sample_file)

    print("\n" + "=" * 60)
    print("[*] [*]!")
    print("=" * 60)


if __name__ == "__main__":
    # [*] [*] [*] [*] main() [*] [*]
    # [*] [*] import[*] [*] [*] [*]
    main()
