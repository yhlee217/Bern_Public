"""
전체 KakaoTalk 대화 감정 분석
모든 메시지를 분석하고 시각화 포함 리포트 생성
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
API_URL = "http://localhost:8000/predict/batch"
BATCH_SIZE = 50

def parse_kakaotalk_file(file_path):
    """카카오톡 대화 파일 전체 파싱"""
    print(f"\n📖 파일 읽는 중: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"✅ 총 {len(lines):,}줄 읽기 완료")

    messages = []
    message_pattern = re.compile(r'^\[(.+?)\] \[(오전|오후) (\d+):(\d+)\] (.+)$')
    current_date = None
    date_pattern = re.compile(r'--------------- (\d{4})년 (\d+)월 (\d+)일')

    for line in lines:
        line = line.strip()

        date_match = date_pattern.search(line)
        if date_match:
            year, month, day = date_match.groups()
            current_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            continue

        msg_match = message_pattern.match(line)
        if msg_match:
            sender, period, hour, minute, content = msg_match.groups()

            if content in ['이모티콘', '사진', '동영상', '파일', '음성메시지', '삭제된 메시지입니다.']:
                continue

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

    print(f"✅ 총 {len(messages):,}개 유효 메시지 추출")
    return messages

def batch_analyze_messages(messages, batch_size=50):
    """배치 API를 사용한 감정 분석"""
    print(f"\n🤖 배치 감정 분석 시작")
    print(f"   - 총 메시지: {len(messages):,}개")
    print(f"   - 배치 크기: {batch_size}개")

    total_batches = (len(messages) + batch_size - 1) // batch_size
    print(f"   - 예상 배치 수: {total_batches}개")
    print(f"   - 예상 소요 시간: ~{total_batches * 1.8 / 60:.1f}분\n")

    analyzed = []
    total = len(messages)
    failed = 0
    total_api_time = 0

    for i in range(0, total, batch_size):
        batch = messages[i:i + batch_size]
        batch_texts = [msg['content'] for msg in batch]
        batch_num = i // batch_size + 1

        # 진행률 표시
        progress = (batch_num / total_batches) * 100
        print(f"[{batch_num}/{total_batches}] {progress:.1f}% | {len(batch_texts)}개 처리중...", end=' ')

        try:
            response = requests.post(
                API_URL,
                json={"texts": batch_texts},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                api_time = result.get('total_time', 0)
                total_api_time += api_time

                for msg, pred in zip(batch, result['results']):
                    msg['sentiment'] = pred['sentiment']
                    msg['confidence'] = pred['confidence']
                    msg['processing_time'] = pred['processing_time']
                    analyzed.append(msg)

                avg_time = api_time / len(batch_texts) * 1000 if batch_texts else 0
                print(f"✅ {api_time:.2f}s ({avg_time:.0f}ms/개)")
            else:
                print(f"❌ HTTP {response.status_code}")
                failed += len(batch)
                for msg in batch:
                    msg['sentiment'] = 'unknown'
                    msg['confidence'] = 0.0
                    msg['processing_time'] = 0.0
                    analyzed.append(msg)

        except Exception as e:
            print(f"❌ {str(e)[:50]}")
            failed += len(batch)
            for msg in batch:
                msg['sentiment'] = 'unknown'
                msg['confidence'] = 0.0
                msg['processing_time'] = 0.0
                analyzed.append(msg)

        if batch_num < total_batches:
            time.sleep(0.1)

    print(f"\n✅ 분석 완료: {len(analyzed):,}개 (실패: {failed}개)")
    print(f"   - 총 API 시간: {total_api_time:.2f}초")
    if total_api_time > 0:
        print(f"   - 처리 속도: {len(analyzed) / total_api_time:.1f}개/초")

    return analyzed

def generate_statistics(analyzed_messages):
    """상세 통계 생성"""
    print("\n📊 통계 생성 중...")

    stats = {
        'total_messages': len(analyzed_messages),
        'by_sentiment': Counter(),
        'by_sender': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}),
        'by_date': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0}),
        'by_hour': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0}),
        'avg_confidence': 0.0,
        'total_chars': 0,
        'sentiment_examples': defaultdict(list),
        'daily_activity': Counter(),
        'hourly_activity': Counter()
    }

    total_confidence = 0
    confidence_count = 0

    for msg in analyzed_messages:
        sentiment = msg['sentiment']
        sender = msg['sender']
        confidence = msg['confidence']
        date = msg['date']
        time_str = msg['time']

        # 감정 통계
        stats['by_sentiment'][sentiment] += 1

        # 발신자 통계
        stats['by_sender'][sender]['total'] += 1
        stats['by_sender'][sender][sentiment] += 1

        # 문자 수
        stats['total_chars'] += msg['length']

        # 날짜별 통계
        if date:
            stats['by_date'][date]['total'] += 1
            stats['by_date'][date][sentiment] += 1
            stats['daily_activity'][date] += 1

        # 시간대별 통계
        if time_str:
            hour = int(time_str.split(':')[0])
            stats['by_hour'][hour]['total'] += 1
            stats['by_hour'][hour][sentiment] += 1
            stats['hourly_activity'][hour] += 1

        # 신뢰도
        if confidence > 0:
            total_confidence += confidence
            confidence_count += 1

        # 샘플 수집
        if confidence > 0.8 and len(stats['sentiment_examples'][sentiment]) < 20:
            stats['sentiment_examples'][sentiment].append({
                'content': msg['content'],
                'sender': sender,
                'confidence': confidence,
                'date': date,
                'time': time_str
            })

    stats['avg_confidence'] = total_confidence / confidence_count if confidence_count > 0 else 0
    stats['avg_message_length'] = stats['total_chars'] / len(analyzed_messages) if analyzed_messages else 0

    return stats

def save_comprehensive_report(analyzed_messages, stats, output_file, total_lines):
    """종합 리포트 저장"""
    print(f"\n💾 종합 리포트 저장 중: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 카카오톡 대화 감정 분석 - 전체 리포트\n\n")
        f.write(f"**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**원본 파일**: KakaoTalk_예원.txt ({total_lines:,}줄)\n\n")
        f.write(f"**분석 메시지**: {stats['total_messages']:,}개 (전체)\n\n")
        f.write("---\n\n")

        # 요약
        f.write("## 📋 요약\n\n")
        f.write(f"- **총 메시지**: {stats['total_messages']:,}개\n")
        f.write(f"- **총 문자 수**: {stats['total_chars']:,}자\n")
        f.write(f"- **평균 길이**: {stats['avg_message_length']:.1f}자\n")
        f.write(f"- **평균 신뢰도**: {stats['avg_confidence']:.1%}\n")
        f.write(f"- **분석 기간**: {min(stats['daily_activity'].keys())} ~ {max(stats['daily_activity'].keys())}\n\n")

        # 감정 분포
        f.write("## 😊 감정 분포\n\n")
        f.write("```\n")
        total = stats['total_messages']
        for sentiment in ['positive', 'negative', 'neutral', 'unknown']:
            count = stats['by_sentiment'].get(sentiment, 0)
            pct = count / total * 100 if total > 0 else 0
            emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐', 'unknown': '❓'}[sentiment]
            bar = '█' * int(pct / 2)
            f.write(f"{emoji} {sentiment:8s}: {bar:<50s} {count:5d}개 ({pct:5.1f}%)\n")
        f.write("```\n\n")

        # 발신자별 통계
        f.write("## 👤 발신자별 통계\n\n")
        for sender, data in sorted(stats['by_sender'].items(), key=lambda x: x[1]['total'], reverse=True):
            total_sender = data['total']
            f.write(f"### {sender}\n\n")
            f.write(f"- **총 메시지**: {total_sender:,}개 ({total_sender/total*100:.1f}%)\n")
            f.write(f"- 😊 긍정: {data['positive']:,}개 ({data['positive']/total_sender*100:.1f}%)\n")
            f.write(f"- 😢 부정: {data['negative']:,}개 ({data['negative']/total_sender*100:.1f}%)\n")
            f.write(f"- 😐 중립: {data['neutral']:,}개 ({data['neutral']/total_sender*100:.1f}%)\n\n")

        # 날짜별 활동
        f.write("## 📅 날짜별 활동 분석\n\n")
        f.write("### 가장 활발했던 날 TOP 10\n\n")
        f.write("| 순위 | 날짜 | 메시지 수 | 😊 긍정 | 😢 부정 | 😐 중립 |\n")
        f.write("|-----|------|----------|---------|---------|----------|\n")

        top_dates = stats['daily_activity'].most_common(10)
        for idx, (date, count) in enumerate(top_dates, 1):
            date_stats = stats['by_date'][date]
            f.write(f"| {idx} | {date} | {count} | {date_stats['positive']} | {date_stats['negative']} | {date_stats['neutral']} |\n")
        f.write("\n")

        # 시간대별 활동
        f.write("## ⏰ 시간대별 활동 분석\n\n")
        f.write("```\n")
        for hour in range(24):
            count = stats['hourly_activity'].get(hour, 0)
            bar = '█' * (count // 50) if count > 0 else ''
            f.write(f"{hour:02d}시: {bar:<40s} {count:4d}개\n")
        f.write("```\n\n")

        # 감정별 샘플
        f.write("## 💬 감정별 대표 메시지 (신뢰도 높은 순)\n\n")

        for sentiment in ['positive', 'negative', 'neutral']:
            emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐'}[sentiment]
            count = stats['by_sentiment'].get(sentiment, 0)
            f.write(f"### {emoji} {sentiment.upper()} ({count}개)\n\n")

            samples = stats['sentiment_examples'].get(sentiment, [])
            samples.sort(key=lambda x: x['confidence'], reverse=True)

            if samples:
                for i, sample in enumerate(samples[:10], 1):
                    f.write(f"{i}. **[{sample['sender']}]** ({sample['confidence']:.1%}) - {sample['date']} {sample['time']}\n")
                    f.write(f"   > {sample['content']}\n\n")
            else:
                f.write("   _(샘플 없음)_\n\n")

        # 분석 정보
        f.write("---\n\n")
        f.write("## ℹ️ 분석 정보\n\n")
        f.write(f"- **사용 모델**: RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)\n")
        f.write(f"- **API**: 배치 처리 ({BATCH_SIZE}개/배치)\n")
        f.write(f"- **전체 분석**: 모든 메시지 분석 완료\n\n")

    print(f"✅ 리포트 저장 완료")

def main():
    print("=" * 70)
    print("🎯 카카오톡 전체 대화 감정 분석")
    print("=" * 70)

    input_file = r"E:\Side Project\KakaoTalk_예원.txt"
    output_report = r"E:\Side Project\full_kakaotalk_analysis_report.md"
    output_json = r"E:\Side Project\full_kakaotalk_analysis_data.json"

    start_time = time.time()

    # 1. 파일 파싱
    messages = parse_kakaotalk_file(input_file)

    if not messages:
        print("❌ 메시지를 찾을 수 없습니다.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        total_lines = len(f.readlines())

    # 2. 감정 분석
    analyzed = batch_analyze_messages(messages, batch_size=BATCH_SIZE)

    # 3. 통계 생성
    stats = generate_statistics(analyzed)

    # 4. 리포트 저장
    save_comprehensive_report(analyzed, stats, output_report, total_lines)

    # 5. JSON 저장
    print(f"💾 JSON 데이터 저장 중: {output_json}")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(analyzed, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 저장 완료")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"✅ 전체 분석 완료!")
    print(f"   - 소요 시간: {elapsed / 60:.1f}분 ({elapsed:.1f}초)")
    print(f"   - 처리 속도: {len(analyzed)/elapsed:.1f}개/초")
    print(f"\n📄 결과:")
    print(f"   - 리포트: {output_report}")
    print(f"   - 데이터: {output_json}")
    print("=" * 70)

if __name__ == "__main__":
    main()
