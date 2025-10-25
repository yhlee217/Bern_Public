"""
01. 단순 규칙 기반 문장 파서 (Simple Baseline Parser)

이 예제는 NLTK와 spaCy를 사용한 규칙 기반 파서를 구현합니다.
- NLTK: 품사 태깅(POS tagging)을 위한 라이브러리
- spaCy: 고급 NLP 기능을 제공하는 라이브러리
- 명사를 주어(Subject)로 가정
- 동사를 술어(Predicate)로 가정
- 나머지는 수식어(Modifiers)로 처리

설치 필요:
pip install nltk spacy
python -m spacy download en_core_web_sm
"""

import os
import re
from typing import List, Tuple, Dict

try:
    import nltk
    from nltk import pos_tag, word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("⚠️ NLTK가 설치되지 않았습니다. 'pip install nltk'로 설치해주세요.")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("⚠️ spaCy가 설치되지 않았습니다. 'pip install spacy'로 설치해주세요.")


class NLTKParser:
    """
    NLTK 기반 Baseline Parser

    특징:
    - NLTK의 품사 태거를 사용하여 문장 구조 파악
    - 첫 번째 명사를 주어로 간주
    - 첫 번째 동사를 술어로 간주
    """

    def __init__(self):
        # Penn Treebank 품사 태그 기준
        self.noun_tags = {'NN', 'NNS', 'NNP', 'NNPS'}
        self.verb_tags = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
        self.adj_tags = {'JJ', 'JJR', 'JJS'}
        self.adv_tags = {'RB', 'RBR', 'RBS'}

        # NLTK 데이터 다운로드 (최초 1회)
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('taggers/averaged_perceptron_tagger')
            except LookupError:
                print("📥 NLTK 데이터 다운로드 중...")
                nltk.download('punkt', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                nltk.download('punkt_tab', quiet=True)
                nltk.download('averaged_perceptron_tagger_eng', quiet=True)

    def parse(self, tokens_with_pos: List[Tuple[str, str]]) -> Dict:
        """
        문장을 파싱하여 구조 추출

        Args:
            tokens_with_pos: [(token, pos_tag), ...] 형식의 리스트

        Returns:
            parsed_structure: {
                'subject': str,
                'predicate': str,
                'modifiers': List[str],
                'adjectives': List[str],
                'adverbs': List[str]
            }
        """
        subject = None
        predicate = None
        modifiers = []
        adjectives = []
        adverbs = []

        for token, pos in tokens_with_pos:
            if pos in self.noun_tags and subject is None:
                subject = token
            elif pos in self.verb_tags and predicate is None:
                predicate = token
            elif pos in self.adj_tags:
                adjectives.append(token)
            elif pos in self.adv_tags:
                adverbs.append(token)
            else:
                if token not in ['.', ',', '!', '?']:  # 구두점 제외
                    modifiers.append(token)

        return {
            'subject': subject,
            'predicate': predicate,
            'modifiers': modifiers,
            'adjectives': adjectives,
            'adverbs': adverbs
        }

    def parse_sentence(self, sentence: str) -> Dict:
        """
        NLTK를 사용하여 문장을 파싱

        Args:
            sentence: 파싱할 문장

        Returns:
            parsed_structure: 파싱된 문장 구조
        """
        if not NLTK_AVAILABLE:
            print("⚠️ NLTK가 설치되지 않았습니다.")
            return self._fallback_parse(sentence)

        # NLTK로 토큰화 및 품사 태깅
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)

        return self.parse(pos_tags)

    def _fallback_parse(self, sentence: str) -> Dict:
        """
        간단한 문장 파싱 (NLTK 없이 fallback)

        이 메서드는 실제 품사 태거 없이 단순 휴리스틱으로 동작합니다.
        """
        words = sentence.lower().replace('.', '').replace('!', '').replace('?', '').split()

        # 간단한 동사 리스트
        common_verbs = {'is', 'are', 'was', 'were', 'run', 'ran', 'jump', 'jumped',
                       'walk', 'walked', 'eat', 'ate', 'sleep', 'slept', 'go', 'went',
                       'make', 'made', 'take', 'took', 'see', 'saw', 'come', 'came'}

        subject = words[0] if words else None
        predicate = None
        modifiers = []

        for word in words[1:]:
            if word in common_verbs and predicate is None:
                predicate = word
            else:
                modifiers.append(word)

        return {
            'subject': subject,
            'predicate': predicate,
            'modifiers': modifiers,
            'adjectives': [],
            'adverbs': []
        }


class SpacyParser:
    """
    spaCy 기반 Parser

    특징:
    - spaCy의 고급 NLP 파이프라인 사용
    - 의존성 파싱(Dependency Parsing)을 활용
    - 문장의 주어와 술어를 더 정확하게 파악
    """

    def __init__(self, model_name='en_core_web_sm'):
        """
        Args:
            model_name: spaCy 모델 이름 (기본값: en_core_web_sm)
        """
        if not SPACY_AVAILABLE:
            print("⚠️ spaCy를 사용할 수 없습니다.")
            self.nlp = None
            return

        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"⚠️ spaCy 모델 '{model_name}'을 찾을 수 없습니다.")
            print(f"   다음 명령으로 설치하세요: python -m spacy download {model_name}")
            self.nlp = None

    def parse_sentence(self, sentence: str) -> Dict:
        """
        spaCy를 사용하여 문장을 파싱

        Args:
            sentence: 파싱할 문장

        Returns:
            parsed_structure: 파싱된 문장 구조
        """
        if self.nlp is None:
            return {
                'subject': None,
                'predicate': None,
                'modifiers': [],
                'adjectives': [],
                'adverbs': [],
                'dependencies': []
            }

        doc = self.nlp(sentence)

        # 주어와 술어 찾기 (의존성 파싱 활용)
        subject = None
        predicate = None
        modifiers = []
        adjectives = []
        adverbs = []
        dependencies = []

        # ROOT 동사 찾기 (주 동사)
        for token in doc:
            if token.dep_ == 'ROOT':
                predicate = token.text

            # 주어 찾기 (nsubj, nsubjpass)
            if token.dep_ in ('nsubj', 'nsubjpass') and subject is None:
                subject = token.text

            # 형용사
            if token.pos_ == 'ADJ':
                adjectives.append(token.text)

            # 부사
            if token.pos_ == 'ADV':
                adverbs.append(token.text)

            # 기타 수식어 (전치사, 관사 등)
            if token.pos_ in ('ADP', 'DET', 'PRON') and token.text.lower() not in ['the', 'a', 'an']:
                modifiers.append(token.text)

            # 의존성 관계 저장
            dependencies.append({
                'text': token.text,
                'pos': token.pos_,
                'dep': token.dep_,
                'head': token.head.text
            })

        return {
            'subject': subject,
            'predicate': predicate,
            'modifiers': modifiers,
            'adjectives': adjectives,
            'adverbs': adverbs,
            'dependencies': dependencies,
            'entities': [(ent.text, ent.label_) for ent in doc.ents]
        }


def demo_nltk_parser():
    """NLTK 파서 예제"""
    print("=" * 60)
    print("예제 1: NLTK를 사용한 파싱")
    print("=" * 60)

    if not NLTK_AVAILABLE:
        print("\n⚠️ NLTK가 설치되지 않아 이 예제를 실행할 수 없습니다.")
        print("   'pip install nltk'로 설치 후 다시 시도해주세요.")
        return

    parser = NLTKParser()

    # 예제 문장들
    sentences = [
        "The cat quickly ran away.",
        "A beautiful bird sings sweetly in the tree.",
        "The old man carefully reads a book.",
        "Children play outside.",
        "The dog barks loudly."
    ]

    for i, sentence in enumerate(sentences, 1):
        print(f"\n문장 {i}: {sentence}")
        result = parser.parse_sentence(sentence)
        print(f"  주어(Subject):      {result['subject']}")
        print(f"  술어(Predicate):    {result['predicate']}")
        print(f"  형용사(Adjectives): {', '.join(result['adjectives']) if result['adjectives'] else 'None'}")
        print(f"  부사(Adverbs):      {', '.join(result['adverbs']) if result['adverbs'] else 'None'}")
        print(f"  수식어(Modifiers):  {', '.join(result['modifiers']) if result['modifiers'] else 'None'}")


def demo_spacy_parser():
    """spaCy 파서 예제"""
    print("\n" + "=" * 60)
    print("예제 2: spaCy를 사용한 파싱")
    print("=" * 60)

    if not SPACY_AVAILABLE:
        print("\n⚠️ spaCy가 설치되지 않아 이 예제를 실행할 수 없습니다.")
        print("   'pip install spacy && python -m spacy download en_core_web_sm'로 설치 후 다시 시도해주세요.")
        return

    parser = SpacyParser()

    if parser.nlp is None:
        print("\n⚠️ spaCy 모델을 로드할 수 없습니다.")
        return

    sentences = [
        "The cat quickly ran away.",
        "A beautiful bird sings sweetly in the tree.",
        "The old man carefully reads a book.",
        "Children play outside happily.",
        "The dog barks loudly at strangers."
    ]

    for i, sentence in enumerate(sentences, 1):
        print(f"\n문장 {i}: {sentence}")
        result = parser.parse_sentence(sentence)
        print(f"  주어(Subject):      {result['subject']}")
        print(f"  술어(Predicate):    {result['predicate']}")
        print(f"  형용사(Adjectives): {', '.join(result['adjectives']) if result['adjectives'] else 'None'}")
        print(f"  부사(Adverbs):      {', '.join(result['adverbs']) if result['adverbs'] else 'None'}")
        print(f"  수식어(Modifiers):  {', '.join(result['modifiers']) if result['modifiers'] else 'None'}")

        # 엔티티가 있으면 출력
        if result.get('entities'):
            entities_str = ', '.join([f"{text}({label})" for text, label in result['entities']])
            print(f"  개체명(Entities):   {entities_str}")


def demo_from_file():
    """파일에서 문장 읽어서 파싱 (NLTK 사용)"""
    print("\n" + "=" * 60)
    print("예제 3: 파일에서 문장 읽어서 파싱 (NLTK)")
    print("=" * 60)

    if not NLTK_AVAILABLE:
        print("\n⚠️ NLTK가 설치되지 않아 이 예제를 실행할 수 없습니다.")
        return

    parser = NLTKParser()

    try:
        # 스크립트 파일이 있는 디렉토리 기준으로 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, 'data', 'sample_sentences.txt')

        with open(data_file, 'r', encoding='utf-8') as f:
            sentences = [line.strip() for line in f if line.strip()]

        for i, sentence in enumerate(sentences, 1):
            print(f"\n문장 {i}: {sentence}")
            result = parser.parse_sentence(sentence)
            print(f"  주어(Subject):      {result['subject']}")
            print(f"  술어(Predicate):    {result['predicate']}")
            print(f"  형용사(Adjectives): {', '.join(result['adjectives']) if result['adjectives'] else 'None'}")
            print(f"  부사(Adverbs):      {', '.join(result['adverbs']) if result['adverbs'] else 'None'}")
            print(f"  수식어(Modifiers):  {', '.join(result['modifiers']) if result['modifiers'] else 'None'}")

    except FileNotFoundError:
        print("\n⚠️  data/sample_sentences.txt 파일을 찾을 수 없습니다.")
        print("   먼저 테스트 데이터 파일을 생성해주세요.")


if __name__ == "__main__":
    print("\n" + "🧩 NLTK & spaCy 기반 Baseline Parser 예제")
    print("=" * 60)

    # 예제 실행
    demo_nltk_parser()
    demo_spacy_parser()
    demo_from_file()

    print("\n" + "=" * 60)
    print("✅ 모든 예제 실행 완료!")
    print("=" * 60)
