"""
KakaoTalk 대화 감정 분석 스크립트
AI 텍스트 감정 분석 서비스를 활용하여 카카오톡 대화 내용의 감정을 분석합니다.
"""

import re
import requests
import json
from collections import defaultdict, Counter
from datetime import datetime
import time

# API 설정
API_URL = "http://localhost:8000/predict"
BATCH_SIZE = 100  # API 호출 배치 크기

def parse_kakaotalk_file(file_path):
    """카카오톡 대화 파일 파싱"""
    print(f"📖 파일 읽는 중: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"✅ 총 {len(lines):,}줄 읽기 완료")

    messages = []
    # 메시지 패턴: [발신자] [시간] 내용
    message_pattern = re.compile(r'^\[(.+?)\] \[(오전|오후) (\d+):(\d+)\] (.+)$')

    current_date = None
    date_pattern = re.compile(r'--------------- (\d{4})년 (\d+)월 (\d+)일')

    for line in lines:
        line = line.strip()

        # 날짜 추출
        date_match = date_pattern.search(line)
        if date_match:
            year, month, day = date_match.groups()
            current_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            continue

        # 메시지 추출
        msg_match = message_pattern.match(line)
        if msg_match:
            sender, period, hour, minute, content = msg_match.groups()

            # 이모티콘, 사진, 동영상 등 제외
            if content in ['이모티콘', '사진', '동영상', '파일', '음성메시지', '삭제된 메시지입니다.']:
                continue

            # 시간 변환 (24시간 형식)
            hour = int(hour)
            if period == '오후' and hour != 12:
                hour += 12
            elif period == '오전' and hour == 12:
                hour = 0

            messages.append({
                'date': current_date,
                'time': f"{hour:02d}:{minute}",
                'sender': sender,
                'content': content,
                'length': len(content)
            })

    print(f"✅ 총 {len(messages):,}개 메시지 파싱 완료")
    return messages

def analyze_sentiment(text):
    """API를 통해 감정 분석 수행"""
    try:
        response = requests.post(
            API_URL,
            json={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"⚠️  API 오류: {e}")
        return None

def batch_analyze_messages(messages):
    """메시지 배치 감정 분석"""
    print(f"\n🤖 감정 분석 시작 (총 {len(messages):,}개 메시지)")

    analyzed = []
    total = len(messages)

    for i, msg in enumerate(messages):
        if (i + 1) % 100 == 0 or i == 0:
            print(f"진행중... {i+1}/{total} ({(i+1)/total*100:.1f}%)")

        result = analyze_sentiment(msg['content'])

        if result:
            msg['sentiment'] = result['sentiment']
            msg['confidence'] = result['confidence']
            analyzed.append(msg)
        else:
            msg['sentiment'] = 'unknown'
            msg['confidence'] = 0.0
            analyzed.append(msg)

        # API 부하 방지를 위한 짧은 대기
        if i % 10 == 0 and i > 0:
            time.sleep(0.1)

    print(f"✅ 감정 분석 완료: {len(analyzed):,}개")
    return analyzed

def generate_statistics(analyzed_messages):
    """통계 생성"""
    print("\n📊 통계 생성 중...")

    stats = {
        'total_messages': len(analyzed_messages),
        'by_sentiment': Counter(),
        'by_sender': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0}),
        'by_date': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0}),
        'avg_confidence': 0.0,
        'total_chars': 0
    }

    total_confidence = 0

    for msg in analyzed_messages:
        sentiment = msg['sentiment']
        sender = msg['sender']
        date = msg['date']
        confidence = msg['confidence']

        # 전체 감정 분포
        stats['by_sentiment'][sentiment] += 1

        # 발신자별 통계
        stats['by_sender'][sender]['total'] += 1
        stats['by_sender'][sender][sentiment] += 1

        # 날짜별 통계
        if date:
            stats['by_date'][date]['total'] += 1
            stats['by_date'][date][sentiment] += 1

        # 신뢰도 및 문자 수
        total_confidence += confidence
        stats['total_chars'] += msg['length']

    stats['avg_confidence'] = total_confidence / len(analyzed_messages) if analyzed_messages else 0
    stats['avg_message_length'] = stats['total_chars'] / len(analyzed_messages) if analyzed_messages else 0

    return stats

def save_results(analyzed_messages, stats, output_file):
    """결과 저장"""
    print(f"\n💾 결과 저장 중: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 카카오톡 대화 감정 분석 결과\n\n")
        f.write(f"**분석 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")

        # 전체 통계
        f.write("## 📊 전체 통계\n\n")
        f.write(f"- **총 메시지 수**: {stats['total_messages']:,}개\n")
        f.write(f"- **총 문자 수**: {stats['total_chars']:,}자\n")
        f.write(f"- **평균 메시지 길이**: {stats['avg_message_length']:.1f}자\n")
        f.write(f"- **평균 신뢰도**: {stats['avg_confidence']:.2%}\n\n")

        # 감정 분포
        f.write("### 감정 분포\n\n")
        for sentiment, count in stats['by_sentiment'].most_common():
            percentage = count / stats['total_messages'] * 100
            f.write(f"- **{sentiment.upper()}**: {count:,}개 ({percentage:.1f}%)\n")
        f.write("\n")

        # 발신자별 통계
        f.write("## 👤 발신자별 통계\n\n")
        for sender, data in sorted(stats['by_sender'].items(), key=lambda x: x[1]['total'], reverse=True):
            f.write(f"### {sender}\n\n")
            f.write(f"- 총 메시지: {data['total']:,}개\n")
            f.write(f"- 긍정: {data['positive']:,}개 ({data['positive']/data['total']*100:.1f}%)\n")
            f.write(f"- 부정: {data['negative']:,}개 ({data['negative']/data['total']*100:.1f}%)\n")
            f.write(f"- 중립: {data['neutral']:,}개 ({data['neutral']/data['total']*100:.1f}%)\n\n")

        # 날짜별 추이 (최근 10일)
        f.write("## 📅 날짜별 감정 추이 (최근 10일)\n\n")
        f.write("| 날짜 | 총 메시지 | 긍정 | 부정 | 중립 |\n")
        f.write("|------|----------|------|------|------|\n")

        sorted_dates = sorted(stats['by_date'].items(), reverse=True)[:10]
        for date, data in sorted_dates:
            f.write(f"| {date} | {data['total']} | {data['positive']} | {data['negative']} | {data['neutral']} |\n")
        f.write("\n")

        # 샘플 메시지
        f.write("## 💬 감정별 샘플 메시지\n\n")

        for sentiment_type in ['positive', 'negative', 'neutral']:
            f.write(f"### {sentiment_type.upper()} 메시지 샘플\n\n")
            samples = [msg for msg in analyzed_messages if msg['sentiment'] == sentiment_type]
            # 신뢰도 높은 순으로 정렬하여 상위 5개
            samples.sort(key=lambda x: x['confidence'], reverse=True)

            for i, msg in enumerate(samples[:5], 1):
                f.write(f"{i}. **[{msg['sender']}]** ({msg['confidence']:.2%}): {msg['content']}\n")
            f.write("\n")

    print(f"✅ 결과 저장 완료: {output_file}")

def save_json_results(analyzed_messages, output_file):
    """JSON 형식으로 상세 결과 저장"""
    print(f"\n💾 JSON 결과 저장 중: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyzed_messages, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON 저장 완료: {output_file}")

def main():
    """메인 실행 함수"""
    import sys
    import io

    # Windows 콘솔 인코딩 문제 해결
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print("🎯 카카오톡 대화 감정 분석 시작")
    print("=" * 60)

    # 파일 경로
    input_file = r"E:\Side Project\KakaoTalk_예원.txt"
    output_report = r"E:\Side Project\kakaotalk_sentiment_report.md"
    output_json = r"E:\Side Project\kakaotalk_sentiment_data.json"

    start_time = time.time()

    # 1. 파일 파싱
    messages = parse_kakaotalk_file(input_file)

    if not messages:
        print("❌ 메시지를 찾을 수 없습니다.")
        return

    # 2. 감정 분석
    analyzed = batch_analyze_messages(messages)

    # 3. 통계 생성
    stats = generate_statistics(analyzed)

    # 4. 결과 저장
    save_results(analyzed, stats, output_report)
    save_json_results(analyzed, output_json)

    # 완료
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"✅ 분석 완료! (소요 시간: {elapsed:.1f}초)")
    print(f"📄 보고서: {output_report}")
    print(f"📄 데이터: {output_json}")
    print("=" * 60)

if __name__ == "__main__":
    main()
