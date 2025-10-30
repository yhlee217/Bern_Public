#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""감정분석 API 테스트 스크립트"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_header(title, color='cyan'):
    colors = {
        'cyan': '\033[96m',
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'end': '\033[0m'
    }
    c = colors.get(color, colors['cyan'])
    print(f"\n{c}{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}{colors['end']}\n")

def test_health():
    """헬스체크 테스트"""
    print_header("헬스체크", 'yellow')
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    print(f"상태: {data['status']}")
    print(f"모델 로드: {data['model_loaded']}")
    print(f"버전: {data['version']}")
    print(f"타임스탬프: {data['timestamp']}")

def test_sentiment(text, test_name, color='cyan'):
    """감정 분석 테스트"""
    print_header(test_name, color)
    response = requests.post(
        f"{BASE_URL}/predict",
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()

    print(f"텍스트: {text}")
    print(f"감정: {data['sentiment']}")
    print(f"신뢰도: {data['confidence']}")
    print(f"처리시간: {data['processing_time']}초")
    if 'model' in data:
        print(f"모델: {data['model']}")
    if 'raw_label' in data:
        print(f"원본 레이블: {data['raw_label']}")

    return data

def main():
    print_header("감정분석 모델 테스트 (개선 버전)", 'cyan')

    # 1. 헬스체크
    test_health()

    # 2. 한글 긍정 테스트
    test_sentiment("오늘 정말 기분이 좋다!", "한글 긍정 테스트", 'green')

    # 3. 한글 부정 테스트
    test_sentiment("정말 최악의 하루였어", "한글 부정 테스트", 'red')

    # 4. 한글 중립 테스트
    test_sentiment("오늘 날씨가 흐립니다", "한글 중립 테스트", 'yellow')

    # 5. 영어 긍정 테스트
    test_sentiment("I am very happy today!", "영어 긍정 테스트", 'green')

    # 6. 영어 부정 테스트
    test_sentiment("This is terrible", "영어 부정 테스트", 'red')

    # 7. 영어 중립 테스트
    test_sentiment("The weather is okay", "영어 중립 테스트", 'yellow')

    print_header("테스트 완료!", 'cyan')

if __name__ == "__main__":
    main()
