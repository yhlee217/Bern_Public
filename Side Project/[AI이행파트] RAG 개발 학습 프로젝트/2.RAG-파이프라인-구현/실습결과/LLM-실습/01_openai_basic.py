"""
실습 1: OpenAI API 기본 호출

목표:
- OpenAI API 클라이언트 설정
- Chat Completion 기본 사용
- 토큰 사용량 확인
"""

import sys
import io

# Windows 콘솔 UTF-8 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

# API 키 설정 (환경 변수 또는 직접 입력)
import os
API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')  # .env 파일 사용 권장

# OpenAI 클라이언트 생성
client = OpenAI(api_key=API_KEY)


def basic_chat_completion():
    """기본 채팅 완성"""
    print("=== 기본 Chat Completion ===\n")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 농업 전문가입니다."},
            {"role": "user", "content": "스마트팜의 주요 이점 3가지를 간단히 설명해주세요."}
        ],
        temperature=0.7,
        max_tokens=300
    )

    # 응답 출력
    answer = response.choices[0].message.content
    print(f"질문: 스마트팜의 주요 이점 3가지를 간단히 설명해주세요.\n")
    print(f"답변:\n{answer}\n")

    # 토큰 사용량
    print(f"토큰 사용량:")
    print(f"  입력: {response.usage.prompt_tokens}")
    print(f"  출력: {response.usage.completion_tokens}")
    print(f"  총합: {response.usage.total_tokens}")


def conversation_example():
    """대화 이력 관리"""
    print("\n\n=== 대화 이력 관리 ===\n")

    messages = [
        {"role": "system", "content": "당신은 스마트팜 전문가입니다."}
    ]

    # 첫 번째 질문
    messages.append({"role": "user", "content": "스마트팜이 뭔가요?"})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    assistant_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_reply})

    print(f"사용자: 스마트팜이 뭔가요?")
    print(f"AI: {assistant_reply}\n")

    # 후속 질문
    messages.append({"role": "user", "content": "비용은 얼마나 드나요?"})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )

    assistant_reply = response.choices[0].message.content
    print(f"사용자: 비용은 얼마나 드나요?")
    print(f"AI: {assistant_reply}")


if __name__ == '__main__':
    try:
        basic_chat_completion()
        conversation_example()
        print("\n\n실습 완료!")
    except Exception as e:
        print(f"오류 발생: {e}")
        print("API 키가 유효한지 확인하세요.")
