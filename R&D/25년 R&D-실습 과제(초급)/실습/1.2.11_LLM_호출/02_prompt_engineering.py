"""
실습 2: 프롬프트 엔지니어링 기초

목표:
- Few-shot Learning 적용
- 시스템 프롬프트 활용
- Temperature 조절
"""

import sys
import io

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI
import os

API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')  # .env 파일 사용 권장

client = OpenAI(api_key=API_KEY)


def few_shot_learning():
    """Few-shot Learning 예시"""
    print("=== Few-shot Learning ===\n")

    prompt = """
다음은 농업 용어를 초보자에게 설명하는 예시입니다:

Q: 양액이 뭔가요?
A: 양액은 식물 생장에 필요한 영양소를 물에 녹인 액체 비료입니다. 스마트팜에서는 자동으로 적정량을 공급합니다.

Q: 광합성이 뭔가요?
A: 광합성은 식물이 빛 에너지를 이용해 이산화탄소와 물로 양분을 만드는 과정입니다.

이제 다음 질문에 같은 방식으로 답변하세요:

Q: 환경 제어가 뭔가요?
A:
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )

    print(prompt)
    print(response.choices[0].message.content)


def temperature_comparison():
    """Temperature 비교"""
    print("\n\n=== Temperature 비교 ===\n")

    question = "스마트팜 회사 이름 5개 제안해주세요."

    # Temperature = 0 (결정적)
    print("Temperature = 0 (결정적, 일관성):")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        temperature=0,
        max_tokens=150
    )
    print(response.choices[0].message.content)

    # Temperature = 1.5 (창의적)
    print("\n\nTemperature = 1.5 (창의적, 다양성):")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
        temperature=1.5,
        max_tokens=150
    )
    print(response.choices[0].message.content)


def system_prompt_role():
    """시스템 프롬프트 역할 부여"""
    print("\n\n=== 시스템 프롬프트 역할 부여 ===\n")

    question = "토마토 재배 시 주의사항은?"

    # 일반 전문가
    print("역할: 일반 전문가")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 농업 전문가입니다."},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=150
    )
    print(response.choices[0].message.content)

    # 초보자 교육자
    print("\n\n역할: 초보자를 위한 친절한 교육자")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 초보 농업인을 교육하는 친절한 선생님입니다. 쉬운 말로 설명하고 구체적인 예시를 들어주세요."},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=150
    )
    print(response.choices[0].message.content)


if __name__ == '__main__':
    try:
        few_shot_learning()
        temperature_comparison()
        system_prompt_role()
        print("\n\n실습 완료!")
    except Exception as e:
        print(f"오류 발생: {e}")
