"""
실습 1: 프롬프트 템플릿 패턴

목표:
- 재사용 가능한 프롬프트 템플릿 작성
- 다양한 태스크 유형별 프롬프트 생성
- 프롬프트 라이브러리 구축
"""

import sys
import io

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class PromptTemplate:
    """프롬프트 템플릿 클래스"""

    @staticmethod
    def structured_template():
        """구조화된 프롬프트 템플릿"""
        return """
[역할]
{role}

[맥락]
{context}

[작업]
{task}

[제약 조건]
{constraints}

[출력 형식]
{output_format}
"""

    @staticmethod
    def few_shot_template():
        """Few-shot 프롬프트 템플릿"""
        return """
다음은 {task_description} 예시입니다:

{examples}

이제 다음에 대해 같은 방식으로 수행하세요:

{input}
"""

    @staticmethod
    def chain_of_thought_template():
        """Chain-of-Thought 프롬프트 템플릿"""
        return """
다음 문제를 단계별로 풀이하세요:

문제: {problem}

단계:
{steps}

풀이:
"""


class PromptLibrary:
    """재사용 가능한 프롬프트 라이브러리"""

    @staticmethod
    def summarize(text, sentences=3):
        """요약 프롬프트"""
        return f"""
다음 문서를 {sentences}문장으로 요약하세요:

{text}

요약:
"""

    @staticmethod
    def classify(text, categories):
        """분류 프롬프트"""
        cats = ", ".join(categories)
        return f"""
다음 텍스트를 카테고리로 분류하세요.

카테고리: {cats}

텍스트: {text}

분류:
"""

    @staticmethod
    def extract_info(text, fields):
        """정보 추출 프롬프트"""
        field_desc = "\n".join([f"- {f}" for f in fields])
        return f"""
다음 텍스트에서 정보를 추출하세요:

텍스트: {text}

추출할 정보:
{field_desc}

결과:
"""

    @staticmethod
    def qa_with_context(context, question):
        """컨텍스트 기반 Q&A 프롬프트"""
        return f"""
다음 컨텍스트를 참고하여 질문에 답변하세요.

[컨텍스트]
{context}

[질문]
{question}

[답변]
"""


def demonstrate_templates():
    """템플릿 사용 예시"""
    print("=== 구조화된 프롬프트 ===\n")

    template = PromptTemplate.structured_template()
    prompt = template.format(
        role="스마트팜 전문가",
        context="초보 농업인을 교육하는 상황",
        task="스마트팜 센서 종류를 설명하세요",
        constraints="- 5가지 이내\n- 각 센서의 기능 포함",
        output_format="불릿 포인트"
    )
    print(prompt)
    print("\n" + "="*60 + "\n")

    # Few-shot 예시
    print("=== Few-shot 프롬프트 ===\n")

    template = PromptTemplate.few_shot_template()
    prompt = template.format(
        task_description="농업 용어 설명",
        examples="""
Q: 양액이 뭔가요?
A: 양액은 식물 생장에 필요한 영양소를 물에 녹인 액체 비료입니다.

Q: 광합성이 뭔가요?
A: 광합성은 식물이 빛 에너지로 양분을 만드는 과정입니다.
""",
        input="Q: 환경 제어가 뭔가요?"
    )
    print(prompt)
    print("\n" + "="*60 + "\n")

    # 프롬프트 라이브러리 사용
    print("=== 프롬프트 라이브러리 사용 ===\n")

    library = PromptLibrary()

    # 요약 프롬프트
    text = "스마트팜은 ICT 기술을 활용한 농업 시스템입니다. 센서로 환경을 측정하고 자동 제어합니다."
    summary_prompt = library.summarize(text, sentences=2)
    print("1. 요약 프롬프트:")
    print(summary_prompt)
    print()

    # 분류 프롬프트
    text = "정부는 스마트팜 보급을 위해 500억원을 편성했다."
    categories = ["기술", "정책", "시장", "환경"]
    classify_prompt = library.classify(text, categories)
    print("2. 분류 프롬프트:")
    print(classify_prompt)
    print()

    # 정보 추출 프롬프트
    text = "경기도 A농장에서는 토마토 생산량이 3톤에서 4.5톤으로 50% 증가했습니다."
    fields = ["위치", "작물", "증가율"]
    extract_prompt = library.extract_info(text, fields)
    print("3. 정보 추출 프롬프트:")
    print(extract_prompt)


if __name__ == '__main__':
    demonstrate_templates()
    print("\n실습 완료!")
    print("\n이 프롬프트들을 LLM API에 전달하여 결과를 확인할 수 있습니다.")
