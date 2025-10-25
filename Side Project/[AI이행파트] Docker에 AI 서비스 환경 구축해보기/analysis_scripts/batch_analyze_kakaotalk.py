"""
KakaoTalk 대화 감정 분석 (배치 처리 최적화 버전)
대용량 데이터 처리를 위한 배치 API 활용
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
BATCH_SIZE = 50  # 한 번에 처리할 메시지 수
MAX_MESSAGES = 1000  # 분석할 최대 메시지 수 (None이면 전체)

def parse_kakaotalk_file(file_path, max_messages=None):
    """카카오톡 대화 파일 파싱"""
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

            # 너무 짧은 메시지 제외
            if len(content) < 2:
                continue

            # 시간 변환
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

            # 최대 메시지 수 제한
            if max_messages and len(messages) >= max_messages:
                break

    print(f"✅ 총 {len(messages):,}개 유효 메시지 추출")
    return messages

def batch_analyze_messages(messages, batch_size=50):
    """배치 API를 사용한 감정 분석"""
    print(f"\n🤖 배치 감정 분석 시작")
    print(f"   - 총 메시지: {len(messages):,}개")
    print(f"   - 배치 크기: {batch_size}개")
    print(f"   - 예상 배치 수: {(len(messages) + batch_size - 1) // batch_size}개\n")

    analyzed = []
    total = len(messages)
    failed = 0
    total_api_time = 0

    # 배치로 분할
    for i in range(0, total, batch_size):
        batch = messages[i:i + batch_size]
        batch_texts = [msg['content'] for msg in batch]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size

        print(f"[배치 {batch_num}/{total_batches}] {len(batch_texts)}개 메시지 처리 중...", end=' ')

        try:
            # 배치 API 호출
            response = requests.post(
                API_URL,
                json={"texts": batch_texts},
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                api_time = result.get('total_time', 0)
                total_api_time += api_time

                # 결과 병합
                for msg, pred in zip(batch, result['results']):
                    msg['sentiment'] = pred['sentiment']
                    msg['confidence'] = pred['confidence']
                    msg['processing_time'] = pred['processing_time']
                    analyzed.append(msg)

                avg_time = api_time / len(batch_texts) * 1000 if batch_texts else 0
                print(f"✅ 완료 ({api_time:.2f}초, 평균 {avg_time:.0f}ms/개)")
            else:
                print(f"❌ 실패 (HTTP {response.status_code})")
                failed += len(batch)
                # 실패한 메시지도 추가 (unknown으로)
                for msg in batch:
                    msg['sentiment'] = 'unknown'
                    msg['confidence'] = 0.0
                    msg['processing_time'] = 0.0
                    analyzed.append(msg)

        except Exception as e:
            print(f"❌ 오류: {e}")
            failed += len(batch)
            for msg in batch:
                msg['sentiment'] = 'unknown'
                msg['confidence'] = 0.0
                msg['processing_time'] = 0.0
                analyzed.append(msg)

        # API 부하 방지
        if batch_num < total_batches:
            time.sleep(0.1)

    print(f"\n✅ 분석 완료")
    print(f"   - 성공: {len(analyzed) - failed:,}개")
    print(f"   - 실패: {failed:,}개")
    print(f"   - 총 API 시간: {total_api_time:.2f}초")
    if total_api_time > 0:
        print(f"   - 처리 속도: {len(analyzed) / total_api_time:.1f}개/초")

    return analyzed

def generate_statistics(analyzed_messages):
    """통계 생성"""
    print("\n📊 통계 생성 중...")

    stats = {
        'total_messages': len(analyzed_messages),
        'by_sentiment': Counter(),
        'by_sender': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}),
        'by_date': defaultdict(lambda: {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0}),
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
        date = msg['date']

        stats['by_sentiment'][sentiment] += 1
        stats['by_sender'][sender]['total'] += 1
        stats['by_sender'][sender][sentiment] += 1
        stats['total_chars'] += msg['length']

        if date:
            stats['by_date'][date]['total'] += 1
            stats['by_date'][date][sentiment] += 1

        if confidence > 0:
            total_confidence += confidence
            confidence_count += 1

        # 고신뢰도 샘플 수집
        if confidence > 0.8 and len(stats['sentiment_examples'][sentiment]) < 10:
            stats['sentiment_examples'][sentiment].append({
                'content': msg['content'],
                'sender': sender,
                'confidence': confidence,
                'date': date
            })

    stats['avg_confidence'] = total_confidence / confidence_count if confidence_count > 0 else 0
    stats['avg_message_length'] = stats['total_chars'] / len(analyzed_messages) if analyzed_messages else 0

    return stats

def save_report(analyzed_messages, stats, output_file, total_lines):
    """마크다운 리포트 저장"""
    print(f"\n💾 리포트 저장 중: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 카카오톡 대화 감정 분석 리포트\n\n")
        f.write(f"**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**원본 파일**: KakaoTalk_예원.txt ({total_lines:,}줄)\n\n")
        f.write(f"**분석 메시지**: {stats['total_messages']:,}개\n\n")
        f.write("---\n\n")

        # 전체 통계
        f.write("## 📊 전체 통계\n\n")
        f.write(f"- **분석 메시지 수**: {stats['total_messages']:,}개\n")
        f.write(f"- **총 문자 수**: {stats['total_chars']:,}자\n")
        f.write(f"- **평균 메시지 길이**: {stats['avg_message_length']:.1f}자\n")
        f.write(f"- **평균 분석 신뢰도**: {stats['avg_confidence']:.1%}\n\n")

        # 감정 분포
        f.write("### 😊 감정 분포\n\n")
        f.write("```\n")
        total = stats['total_messages']
        for sentiment in ['positive', 'negative', 'neutral', 'unknown']:
            count = stats['by_sentiment'].get(sentiment, 0)
            pct = count / total * 100 if total > 0 else 0
            emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐', 'unknown': '❓'}.get(sentiment, '❓')
            bar = '█' * int(pct / 2)
            f.write(f"{emoji} {sentiment:8s}: {bar:<50s} {count:4d}개 ({pct:5.1f}%)\n")
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

        # 날짜별 추이
        if stats['by_date']:
            f.write("## 📅 날짜별 감정 추이\n\n")
            f.write("| 날짜 | 총 메시지 | 😊 긍정 | 😢 부정 | 😐 중립 |\n")
            f.write("|------|----------|---------|---------|----------|\n")

            sorted_dates = sorted(stats['by_date'].items())[:20]  # 최근 20일
            for date, data in sorted_dates:
                f.write(f"| {date} | {data['total']} | {data['positive']} | {data['negative']} | {data['neutral']} |\n")
            f.write("\n")

        # 감정별 샘플
        f.write("## 💬 감정별 샘플 메시지 (신뢰도 높은 순)\n\n")

        for sentiment in ['positive', 'negative', 'neutral']:
            emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐'}[sentiment]
            f.write(f"### {emoji} {sentiment.upper()}\n\n")

            samples = stats['sentiment_examples'].get(sentiment, [])
            samples.sort(key=lambda x: x['confidence'], reverse=True)

            if samples:
                for i, sample in enumerate(samples[:5], 1):
                    f.write(f"{i}. **[{sample['sender']}]** ({sample['confidence']:.1%})\n")
                    f.write(f"   > {sample['content']}\n")
                    if sample['date']:
                        f.write(f"   > *{sample['date']}*\n")
                    f.write("\n")
            else:
                f.write("   _(샘플 없음)_\n\n")

        # 분석 정보
        f.write("---\n\n")
        f.write("## ℹ️ 분석 정보\n\n")
        f.write(f"- **사용 모델**: RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)\n")
        f.write(f"- **API 엔드포인트**: {API_URL}\n")
        f.write(f"- **배치 크기**: {BATCH_SIZE}개\n")
        f.write(f"- **처리 방식**: 배치 API를 통한 효율적 처리\n\n")

    print(f"✅ 리포트 저장 완료")

def save_json_data(analyzed_messages, output_file):
    """JSON 데이터 저장"""
    print(f"💾 JSON 데이터 저장 중: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analyzed_messages, f, ensure_ascii=False, indent=2)

    print(f"✅ JSON 저장 완료")

def main():
    print("=" * 70)
    print("🎯 카카오톡 대화 감정 분석 (배치 처리 최적화 버전)")
    print("=" * 70)

    # 파일 경로
    input_file = r"E:\Side Project\KakaoTalk_예원.txt"
    output_report = r"E:\Side Project\kakaotalk_analysis_report.md"
    output_json = r"E:\Side Project\kakaotalk_analysis_data.json"

    start_time = time.time()

    # 1. 파일 파싱
    messages = parse_kakaotalk_file(input_file, max_messages=MAX_MESSAGES)

    if not messages:
        print("❌ 메시지를 찾을 수 없습니다.")
        return

    # 원본 파일 라인 수
    with open(input_file, 'r', encoding='utf-8') as f:
        total_lines = len(f.readlines())

    # 2. 배치 감정 분석
    analyzed = batch_analyze_messages(messages, batch_size=BATCH_SIZE)

    # 3. 통계 생성
    stats = generate_statistics(analyzed)

    # 4. 결과 저장
    save_report(analyzed, stats, output_report, total_lines)
    save_json_data(analyzed, output_json)

    # 완료
    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"✅ 전체 분석 완료!")
    print(f"   - 소요 시간: {elapsed:.1f}초")
    print(f"   - 처리 속도: {len(analyzed)/elapsed:.1f}개/초")
    print(f"\n📄 결과 파일:")
    print(f"   - 리포트: {output_report}")
    print(f"   - 데이터: {output_json}")
    print("=" * 70)

if __name__ == "__main__":
    main()
