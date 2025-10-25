"""
KakaoTalk 대화 감정 분석 스크립트 (샘플 버전)
빠른 분석을 위해 샘플 메시지만 분석합니다.
"""

import re
import requests
import json
from collections import defaultdict, Counter
from datetime import datetime
import time
import sys
import io

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# API 설정
API_URL = "http://localhost:8000/predict"
SAMPLE_SIZE = 500  # 분석할 메시지 샘플 크기

def parse_kakaotalk_file(file_path, limit=None):
    """카카오톡 대화 파일 파싱"""
    print(f"📖 파일 읽는 중: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"✅ 총 {len(lines):,}줄 읽기 완료")

    messages = []
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

            # 이모티콘, 사진 등 제외
            if content in ['이모티콘', '사진', '동영상', '파일', '음성메시지', '삭제된 메시지입니다.']:
                continue

            # 너무 짧은 메시지 제외 (분석 의미 없음)
            if len(content) < 2:
                continue

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

            # 제한이 있으면 조기 종료
            if limit and len(messages) >= limit:
                break

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
        return None

def batch_analyze_messages(messages):
    """메시지 배치 감정 분석"""
    print(f"\n🤖 감정 분석 시작 (총 {len(messages):,}개 메시지)")

    analyzed = []
    total = len(messages)
    failed = 0

    for i, msg in enumerate(messages):
        if (i + 1) % 50 == 0 or i == 0 or (i + 1) == total:
            percentage = (i + 1) / total * 100
            print(f"진행중... {i+1}/{total} ({percentage:.1f}%)")

        result = analyze_sentiment(msg['content'])

        if result:
            msg['sentiment'] = result['sentiment']
            msg['confidence'] = result['confidence']
            msg['processing_time'] = result.get('processing_time', 0)
        else:
            msg['sentiment'] = 'unknown'
            msg['confidence'] = 0.0
            msg['processing_time'] = 0
            failed += 1

        analyzed.append(msg)

        # API 부하 방지
        if i % 5 == 0 and i > 0:
            time.sleep(0.05)

    print(f"✅ 감정 분석 완료: {len(analyzed):,}개 (실패: {failed}개)")
    return analyzed

def generate_statistics(analyzed_messages):
    """통계 생성"""
    print("\n📊 통계 생성 중...")

    stats = {
        'total_messages': len(analyzed_messages),
        'by_sentiment': Counter(),
        'by_sender': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}),
        'avg_confidence': 0.0,
        'total_chars': 0,
        'sentiment_examples': defaultdict(list)
    }

    total_confidence = 0
    confidence_count = 0

    for msg in analyzed_messages:
        sentiment = msg['sentiment']
        sender = msg['sender']
        confidence = msg['confidence']

        stats['by_sentiment'][sentiment] += 1
        stats['by_sender'][sender]['total'] += 1
        stats['by_sender'][sender][sentiment] += 1
        stats['total_chars'] += msg['length']

        if confidence > 0:
            total_confidence += confidence
            confidence_count += 1

        # 높은 신뢰도의 샘플 메시지 수집
        if confidence > 0.8 and len(stats['sentiment_examples'][sentiment]) < 10:
            stats['sentiment_examples'][sentiment].append({
                'content': msg['content'],
                'sender': sender,
                'confidence': confidence,
                'date': msg['date']
            })

    stats['avg_confidence'] = total_confidence / confidence_count if confidence_count > 0 else 0
    stats['avg_message_length'] = stats['total_chars'] / len(analyzed_messages) if analyzed_messages else 0

    return stats

def save_results(analyzed_messages, stats, output_file, sample_size, total_messages):
    """결과 저장"""
    print(f"\n💾 결과 저장 중: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 카카오톡 대화 감정 분석 결과\n\n")
        f.write(f"**분석 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**분석 방식**: 샘플 분석 (전체 {total_messages:,}개 중 {sample_size:,}개 샘플)\n\n")
        f.write("---\n\n")

        # 전체 통계
        f.write("## 📊 전체 통계\n\n")
        f.write(f"- **분석 메시지 수**: {stats['total_messages']:,}개\n")
        f.write(f"- **총 문자 수**: {stats['total_chars']:,}자\n")
        f.write(f"- **평균 메시지 길이**: {stats['avg_message_length']:.1f}자\n")
        f.write(f"- **평균 분석 신뢰도**: {stats['avg_confidence']:.1%}\n\n")

        # 감정 분포
        f.write("### 😊 감정 분포\n\n")
        total = stats['total_messages']
        for sentiment, count in stats['by_sentiment'].most_common():
            percentage = count / total * 100
            emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐', 'unknown': '❓'}.get(sentiment, '❓')
            f.write(f"- {emoji} **{sentiment.upper()}**: {count:,}개 ({percentage:.1f}%)\n")
        f.write("\n")

        # 발신자별 통계
        f.write("## 👤 발신자별 통계\n\n")
        for sender, data in sorted(stats['by_sender'].items(), key=lambda x: x[1]['total'], reverse=True):
            f.write(f"### {sender}\n\n")
            total_sender = data['total']
            f.write(f"- **총 메시지**: {total_sender:,}개\n")
            f.write(f"- 😊 긍정: {data['positive']:,}개 ({data['positive']/total_sender*100:.1f}%)\n")
            f.write(f"- 😢 부정: {data['negative']:,}개 ({data['negative']/total_sender*100:.1f}%)\n")
            f.write(f"- 😐 중립: {data['neutral']:,}개 ({data['neutral']/total_sender*100:.1f}%)\n\n")

        # 감정별 샘플 메시지
        f.write("## 💬 감정별 샘플 메시지 (신뢰도 높은 순)\n\n")

        for sentiment_type in ['positive', 'negative', 'neutral']:
            emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐'}.get(sentiment_type, '')
            f.write(f"### {emoji} {sentiment_type.upper()} 메시지\n\n")

            samples = stats['sentiment_examples'].get(sentiment_type, [])
            samples.sort(key=lambda x: x['confidence'], reverse=True)

            if samples:
                for i, sample in enumerate(samples[:5], 1):
                    f.write(f"{i}. **[{sample['sender']}]** ({sample['confidence']:.1%})\n")
                    f.write(f"   > {sample['content']}\n\n")
            else:
                f.write("   _(샘플 없음)_\n\n")

        # 분석 정보
        f.write("---\n\n")
        f.write("## ℹ️ 분석 정보\n\n")
        f.write(f"- **사용 모델**: RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)\n")
        f.write(f"- **API 서버**: {API_URL}\n")
        f.write(f"- **샘플링 방식**: 파일 시작부터 순차적으로 {sample_size:,}개 추출\n")
        f.write(f"- **신뢰도 기준**: 80% 이상을 고신뢰도로 분류\n\n")

    print(f"✅ 결과 저장 완료")

def main():
    print("=" * 60)
    print("🎯 카카오톡 대화 감정 분석 (샘플 버전)")
    print("=" * 60)

    # 파일 경로
    input_file = r"E:\Side Project\KakaoTalk_예원.txt"
    output_report = r"E:\Side Project\kakaotalk_sentiment_report.md"

    start_time = time.time()

    # 1. 파일 파싱 (샘플만)
    print(f"\n📌 샘플 크기: {SAMPLE_SIZE:,}개 메시지")
    messages = parse_kakaotalk_file(input_file, limit=SAMPLE_SIZE * 3)  # 여유있게 추출

    if not messages:
        print("❌ 메시지를 찾을 수 없습니다.")
        return

    # 실제 메시지 수가 샘플 크기보다 작으면 전체 분석
    actual_sample_size = min(SAMPLE_SIZE, len(messages))
    sample_messages = messages[:actual_sample_size]
    total_messages = len(messages)

    print(f"📊 샘플 추출: {actual_sample_size:,}개 메시지 (전체: {total_messages:,}개)")

    # 2. 감정 분석
    analyzed = batch_analyze_messages(sample_messages)

    # 3. 통계 생성
    stats = generate_statistics(analyzed)

    # 4. 결과 저장
    save_results(analyzed, stats, output_report, actual_sample_size, total_messages)

    # 완료
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"✅ 분석 완료! (소요 시간: {elapsed:.1f}초)")
    print(f"📄 보고서: {output_report}")
    print("=" * 60)
    print(f"\n💡 Tip: 전체 분석을 원하시면 SAMPLE_SIZE를 늘려주세요.")

if __name__ == "__main__":
    main()
