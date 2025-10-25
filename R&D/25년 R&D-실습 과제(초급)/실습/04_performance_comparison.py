"""
04. 성능 비교 예제 (Baseline vs Advanced Parser)

Baseline Parser와 고급 Parser의 성능을 비교합니다.
- 파싱 속도
- 정확도
- 메모리 사용량
"""

import time
import re
from typing import List, Tuple, Dict
from collections import defaultdict


class BaselineParser:
    """
    단순 규칙 기반 Baseline Parser
    - 정규식과 간단한 휴리스틱 사용
    """

    def __init__(self):
        self.verb_pattern = re.compile(r'\b(is|are|was|were|run|ran|jump|jumped|walk|walked)\b')

    def parse(self, sentence: str) -> Dict:
        """간단한 규칙으로 문장 파싱"""
        words = sentence.lower().replace('.', '').split()

        if not words:
            return {'subject': None, 'predicate': None, 'modifiers': []}

        # 첫 단어를 주어로
        subject = words[0]

        # 동사 찾기
        predicate = None
        for word in words:
            if self.verb_pattern.match(word):
                predicate = word
                break

        # 나머지는 수식어
        modifiers = [w for w in words[1:] if w != predicate]

        return {
            'subject': subject,
            'predicate': predicate,
            'modifiers': modifiers
        }


class FrequencyBasedParser:
    """
    빈도 기반 통계 Parser
    - 훈련 데이터에서 패턴 학습
    - 가장 빈번한 패턴 적용
    """

    def __init__(self):
        self.patterns = defaultdict(int)
        self.trained = False

    def train(self, sentences: List[str]):
        """문장 패턴 학습"""
        for sentence in sentences:
            words = sentence.lower().replace('.', '').split()
            if len(words) >= 2:
                # 간단한 패턴: 첫 2개 단어의 조합
                pattern = f"{words[0]}_{words[1]}"
                self.patterns[pattern] += 1
        self.trained = True

    def parse(self, sentence: str) -> Dict:
        """학습된 패턴 기반 파싱"""
        words = sentence.lower().replace('.', '').split()

        if not words:
            return {'subject': None, 'predicate': None, 'modifiers': []}

        # 패턴 매칭
        if len(words) >= 2:
            pattern = f"{words[0]}_{words[1]}"
            if pattern in self.patterns:
                # 패턴이 있으면 첫 단어를 주어, 두 번째를 술어로
                return {
                    'subject': words[0],
                    'predicate': words[1],
                    'modifiers': words[2:]
                }

        # 패턴이 없으면 기본 규칙
        return {
            'subject': words[0] if words else None,
            'predicate': words[1] if len(words) > 1 else None,
            'modifiers': words[2:] if len(words) > 2 else []
        }


class RuleBasedParser:
    """
    향상된 규칙 기반 Parser
    - 더 많은 규칙과 예외 처리
    """

    def __init__(self):
        self.verbs = {'is', 'are', 'was', 'were', 'run', 'ran', 'runs',
                     'jump', 'jumped', 'jumps', 'walk', 'walked', 'walks',
                     'eat', 'ate', 'eats', 'sleep', 'slept', 'sleeps'}
        self.determiners = {'the', 'a', 'an'}

    def parse(self, sentence: str) -> Dict:
        """규칙 기반 파싱"""
        words = sentence.lower().replace('.', '').replace(',', '').split()

        if not words:
            return {'subject': None, 'predicate': None, 'modifiers': []}

        # 관사 제거 후 첫 단어를 주어로
        subject_idx = 0
        if words[0] in self.determiners and len(words) > 1:
            subject_idx = 1

        subject = words[subject_idx]

        # 동사 찾기
        predicate = None
        predicate_idx = -1
        for i, word in enumerate(words):
            if word in self.verbs:
                predicate = word
                predicate_idx = i
                break

        # 수식어 분류
        modifiers_before = words[subject_idx + 1:predicate_idx] if predicate_idx > subject_idx + 1 else []
        modifiers_after = words[predicate_idx + 1:] if predicate_idx != -1 and predicate_idx < len(words) - 1 else []

        return {
            'subject': subject,
            'predicate': predicate,
            'modifiers': modifiers_before + modifiers_after
        }


def benchmark_parser(parser, sentences: List[str], parser_name: str) -> Dict:
    """
    파서 성능 측정

    Returns:
        성능 통계
    """
    print(f"\n{'=' * 60}")
    print(f"🔍 {parser_name} 성능 측정")
    print(f"{'=' * 60}")

    # 속도 측정
    start_time = time.time()

    results = []
    for sentence in sentences:
        result = parser.parse(sentence)
        results.append(result)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # 통계 계산
    total_sentences = len(sentences)
    parsed_subjects = sum(1 for r in results if r['subject'] is not None)
    parsed_predicates = sum(1 for r in results if r['predicate'] is not None)

    avg_time_per_sentence = (elapsed_time / total_sentences) * 1000  # ms

    stats = {
        'parser_name': parser_name,
        'total_time': elapsed_time,
        'avg_time_per_sentence': avg_time_per_sentence,
        'total_sentences': total_sentences,
        'parsed_subjects': parsed_subjects,
        'parsed_predicates': parsed_predicates,
        'subject_rate': (parsed_subjects / total_sentences) * 100,
        'predicate_rate': (parsed_predicates / total_sentences) * 100,
    }

    # 결과 출력
    print(f"\n📊 성능 지표:")
    print(f"  전체 처리 시간:        {elapsed_time:.4f}초")
    print(f"  문장당 평균 시간:      {avg_time_per_sentence:.4f}ms")
    print(f"  초당 처리 문장 수:     {total_sentences / elapsed_time:.0f}개/초")

    print(f"\n📈 파싱 성공률:")
    print(f"  주어 파싱 성공:        {parsed_subjects}/{total_sentences} ({stats['subject_rate']:.1f}%)")
    print(f"  술어 파싱 성공:        {parsed_predicates}/{total_sentences} ({stats['predicate_rate']:.1f}%)")

    # 샘플 결과 출력
    print(f"\n📝 샘플 파싱 결과 (처음 5개):")
    for i, (sentence, result) in enumerate(zip(sentences[:5], results[:5]), 1):
        print(f"  {i}. \"{sentence}\"")
        print(f"     주어: {result['subject']}, 술어: {result['predicate']}")

    return stats


def compare_parsers():
    """여러 파서 성능 비교"""
    print("\n" + "=" * 70)
    print("📊 Baseline Parser vs Advanced Parser 성능 비교")
    print("=" * 70)

    # 테스트 문장 생성
    sentences = [
        "The cat runs quickly.",
        "A dog jumps high.",
        "The bird sings beautifully.",
        "Children play outside.",
        "The man walks slowly.",
        "A car runs fast.",
        "The teacher is kind.",
        "Students are studying.",
        "The sun is bright.",
        "Flowers are blooming.",
    ] * 100  # 1000개 문장

    print(f"\n📌 테스트 데이터: {len(sentences)}개 문장")

    # 1. Baseline Parser 테스트
    baseline_parser = BaselineParser()
    baseline_stats = benchmark_parser(baseline_parser, sentences, "Baseline Parser")

    # 2. Frequency-based Parser 테스트 (먼저 학습)
    freq_parser = FrequencyBasedParser()
    training_data = sentences[:500]  # 절반으로 학습
    print(f"\n🎓 Frequency-based Parser 학습 중... ({len(training_data)}개 문장)")
    freq_parser.train(training_data)
    freq_stats = benchmark_parser(freq_parser, sentences, "Frequency-based Parser")

    # 3. Rule-based Parser 테스트
    rule_parser = RuleBasedParser()
    rule_stats = benchmark_parser(rule_parser, sentences, "Rule-based Parser")

    # 비교 결과 요약
    print("\n" + "=" * 70)
    print("📊 최종 비교 결과")
    print("=" * 70)

    all_stats = [baseline_stats, freq_stats, rule_stats]

    print(f"\n{'Parser':<25} {'속도(ms)':<12} {'주어성공률':<12} {'술어성공률':<12}")
    print("-" * 70)
    for stats in all_stats:
        print(f"{stats['parser_name']:<25} "
              f"{stats['avg_time_per_sentence']:<12.4f} "
              f"{stats['subject_rate']:<12.1f}% "
              f"{stats['predicate_rate']:<12.1f}%")

    # 최고 성능 파서 찾기
    print(f"\n🏆 성능 순위:")
    fastest = min(all_stats, key=lambda x: x['avg_time_per_sentence'])
    print(f"  가장 빠른 파서:    {fastest['parser_name']} ({fastest['avg_time_per_sentence']:.4f}ms)")

    most_accurate = max(all_stats, key=lambda x: (x['subject_rate'] + x['predicate_rate']) / 2)
    print(f"  가장 정확한 파서:  {most_accurate['parser_name']} "
          f"(평균 {(most_accurate['subject_rate'] + most_accurate['predicate_rate']) / 2:.1f}%)")


def accuracy_test():
    """정답 데이터와 비교하여 정확도 측정"""
    print("\n" + "=" * 70)
    print("🎯 정확도 테스트 (Ground Truth 비교)")
    print("=" * 70)

    # 정답 라벨이 있는 테스트 데이터
    test_data = [
        ("The cat runs.", {'subject': 'cat', 'predicate': 'runs'}),
        ("A dog jumps.", {'subject': 'dog', 'predicate': 'jumps'}),
        ("Birds are singing.", {'subject': 'birds', 'predicate': 'are'}),
        ("The child is playing.", {'subject': 'child', 'predicate': 'is'}),
        ("Trees grow tall.", {'subject': 'trees', 'predicate': 'grow'}),
    ]

    parsers = [
        ("Baseline", BaselineParser()),
        ("Rule-based", RuleBasedParser()),
    ]

    for parser_name, parser in parsers:
        print(f"\n{parser_name} Parser 정확도:")

        correct_subject = 0
        correct_predicate = 0

        for sentence, ground_truth in test_data:
            result = parser.parse(sentence)

            if result['subject'] == ground_truth['subject']:
                correct_subject += 1
            if result['predicate'] == ground_truth['predicate']:
                correct_predicate += 1

        total = len(test_data)
        print(f"  주어 정확도:  {correct_subject}/{total} ({correct_subject/total*100:.1f}%)")
        print(f"  술어 정확도:  {correct_predicate}/{total} ({correct_predicate/total*100:.1f}%)")


if __name__ == "__main__":
    print("\n⚡ Parser 성능 비교 및 벤치마크")
    print("=" * 70)

    # 성능 비교 실행
    compare_parsers()

    # 정확도 테스트
    accuracy_test()

    print("\n" + "=" * 70)
    print("✅ 모든 벤치마크 완료!")
    print("=" * 70)
    print("\n💡 결론:")
    print("  - Baseline Parser는 가장 단순하지만 기본적인 기능 제공")
    print("  - Rule-based Parser는 더 많은 규칙으로 정확도 향상")
    print("  - Frequency-based Parser는 학습 데이터를 활용하여 패턴 인식")
    print("  - 실제 프로젝트에서는 Baseline으로 시작하여 점진적으로 개선")
    print("=" * 70)
