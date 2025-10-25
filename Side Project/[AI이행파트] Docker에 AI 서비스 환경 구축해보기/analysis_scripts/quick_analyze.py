"""
빠른 카카오톡 감정 분석 (소규모 샘플)
"""
import re
import requests
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://localhost:8000/predict"

def parse_messages(file_path, limit=200):
    """메시지 파싱"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    messages = []
    pattern = re.compile(r'^\[(.+?)\] \[(오전|오후) (\d+):(\d+)\] (.+)$')

    for line in lines:
        line = line.strip()
        match = pattern.match(line)
        if match:
            sender, _, _, _, content = match.groups()
            if content not in ['이모티콘', '사진', '동영상', '파일'] and len(content) > 2:
                messages.append({'sender': sender, 'content': content})
                if len(messages) >= limit:
                    break

    return messages

def analyze(text):
    """감정 분석"""
    try:
        r = requests.post(API_URL, json={"text": text}, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def main():
    print("🎯 카카오톡 감정 분석 (빠른 샘플 테스트)\n")

    file_path = r"E:\Side Project\KakaoTalk_예원.txt"
    print(f"📖 파일 파싱 중...")
    messages = parse_messages(file_path, limit=200)
    print(f"✅ {len(messages)}개 메시지 추출\n")

    print("🤖 감정 분석 중...\n")
    results = {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}
    sender_stats = {}
    samples = {'positive': [], 'negative': [], 'neutral': []}

    for i, msg in enumerate(messages, 1):
        print(f"[{i}/{len(messages)}] 분석 중...", end='\r')

        result = analyze(msg['content'])

        if result:
            sentiment = result['sentiment']
            confidence = result['confidence']
            results[sentiment] += 1

            sender = msg['sender']
            if sender not in sender_stats:
                sender_stats[sender] = {'positive': 0, 'negative': 0, 'neutral': 0}
            sender_stats[sender][sentiment] += 1

            # 샘플 수집
            if len(samples[sentiment]) < 5 and confidence > 0.7:
                samples[sentiment].append({
                    'content': msg['content'],
                    'sender': sender,
                    'confidence': confidence
                })
        else:
            results['unknown'] += 1

    print("\n")

    # 결과 출력
    print("=" * 60)
    print("📊 분석 결과\n")

    total = sum(results.values())
    print(f"총 메시지: {total}개\n")

    print("감정 분포:")
    for sentiment, count in results.items():
        pct = count / total * 100 if total > 0 else 0
        emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐', 'unknown': '❓'}[sentiment]
        print(f"  {emoji} {sentiment.upper()}: {count}개 ({pct:.1f}%)")

    print("\n발신자별 통계:")
    for sender, stats in sorted(sender_stats.items(), key=lambda x: sum(x[1].values()), reverse=True):
        total_s = sum(stats.values())
        print(f"  [{sender}] 총 {total_s}개")
        print(f"    긍정: {stats['positive']}개, 부정: {stats['negative']}개, 중립: {stats['neutral']}개")

    print("\n💬 샘플 메시지:")
    for sentiment in ['positive', 'negative', 'neutral']:
        emoji = {'positive': '😊', 'negative': '😢', 'neutral': '😐'}[sentiment]
        print(f"\n{emoji} {sentiment.upper()}:")
        for sample in samples[sentiment]:
            print(f"  [{sample['sender']}] ({sample['confidence']:.0%}) {sample['content']}")

    print("\n" + "=" * 60)
    print(f"✅ 완료! 샘플 {total}개 분석됨")

if __name__ == "__main__":
    main()
