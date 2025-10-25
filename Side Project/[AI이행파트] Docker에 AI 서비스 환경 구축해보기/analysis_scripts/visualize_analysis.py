"""
카카오톡 감정 분석 시각화 모듈
분석 데이터를 그래프와 차트로 시각화
"""

import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter, defaultdict
from datetime import datetime
import sys
import io

# Windows 콘솔 인코딩
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def load_analysis_data(json_file):
    """분석 데이터 로드"""
    print(f"📖 데이터 로딩 중: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✅ {len(data):,}개 메시지 로드 완료")
    return data

def prepare_statistics(data):
    """통계 데이터 준비"""
    print("\n📊 통계 계산 중...")

    stats = {
        'sentiment_counts': Counter(),
        'sender_stats': defaultdict(lambda: Counter()),
        'daily_counts': Counter(),
        'daily_sentiment': defaultdict(lambda: Counter()),
        'hourly_counts': Counter(),
        'hourly_sentiment': defaultdict(lambda: Counter())
    }

    for msg in data:
        sentiment = msg.get('sentiment', 'unknown')
        sender = msg.get('sender', 'Unknown')
        date = msg.get('date')
        time_str = msg.get('time', '00:00')

        # 감정 통계
        stats['sentiment_counts'][sentiment] += 1

        # 발신자별 감정
        stats['sender_stats'][sender][sentiment] += 1

        # 날짜별 통계
        if date:
            stats['daily_counts'][date] += 1
            stats['daily_sentiment'][date][sentiment] += 1

        # 시간대별 통계
        hour = int(time_str.split(':')[0])
        stats['hourly_counts'][hour] += 1
        stats['hourly_sentiment'][hour][sentiment] += 1

    return stats

def create_sentiment_pie_chart(stats, output_file):
    """감정 분포 파이 차트"""
    print("\n🎨 감정 분포 파이 차트 생성 중...")

    sentiments = ['positive', 'negative', 'neutral']
    counts = [stats['sentiment_counts'].get(s, 0) for s in sentiments]
    labels = ['긍정 😊', '부정 😢', '중립 😐']
    colors = ['#90EE90', '#FFB6C1', '#B0C4DE']

    plt.figure(figsize=(10, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('카카오톡 대화 감정 분포', fontsize=16, fontweight='bold')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ 저장: {output_file}")

def create_sender_bar_chart(stats, output_file):
    """발신자별 감정 분포 막대 그래프"""
    print("🎨 발신자별 감정 분포 막대 그래프 생성 중...")

    senders = list(stats['sender_stats'].keys())
    positive = [stats['sender_stats'][s]['positive'] for s in senders]
    negative = [stats['sender_stats'][s]['negative'] for s in senders]
    neutral = [stats['sender_stats'][s]['neutral'] for s in senders]

    x = range(len(senders))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar([i - width for i in x], positive, width, label='긍정 😊', color='#90EE90')
    ax.bar(x, negative, width, label='부정 😢', color='#FFB6C1')
    ax.bar([i + width for i in x], neutral, width, label='중립 😐', color='#B0C4DE')

    ax.set_xlabel('발신자', fontsize=12)
    ax.set_ylabel('메시지 수', fontsize=12)
    ax.set_title('발신자별 감정 분포', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(senders)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ 저장: {output_file}")

def create_daily_activity_chart(stats, output_file):
    """날짜별 활동 추이 그래프"""
    print("🎨 날짜별 활동 추이 그래프 생성 중...")

    # 날짜 정렬
    sorted_dates = sorted(stats['daily_counts'].items())
    dates = [d[0] for d in sorted_dates]
    counts = [d[1] for d in sorted_dates]

    # 감정별 데이터
    positive = [stats['daily_sentiment'][d]['positive'] for d in dates]
    negative = [stats['daily_sentiment'][d]['negative'] for d in dates]
    neutral = [stats['daily_sentiment'][d]['neutral'] for d in dates]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

    # 전체 활동량
    ax1.plot(dates, counts, marker='o', linewidth=2, markersize=4, color='#4169E1')
    ax1.fill_between(dates, counts, alpha=0.3, color='#4169E1')
    ax1.set_ylabel('메시지 수', fontsize=12)
    ax1.set_title('날짜별 메시지 활동량', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)

    # 감정별 스택 차트
    ax2.fill_between(dates, 0, positive, label='긍정 😊', alpha=0.7, color='#90EE90')
    ax2.fill_between(dates, positive, [p+n for p,n in zip(positive, negative)],
                     label='부정 😢', alpha=0.7, color='#FFB6C1')
    ax2.fill_between(dates, [p+n for p,n in zip(positive, negative)],
                     [p+n+ne for p,n,ne in zip(positive, negative, neutral)],
                     label='중립 😐', alpha=0.7, color='#B0C4DE')

    ax2.set_xlabel('날짜', fontsize=12)
    ax2.set_ylabel('메시지 수', fontsize=12)
    ax2.set_title('날짜별 감정 분포', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ 저장: {output_file}")

def create_hourly_heatmap(stats, output_file):
    """시간대별 활동 히트맵"""
    print("🎨 시간대별 활동 히트맵 생성 중...")

    hours = list(range(24))
    counts = [stats['hourly_counts'].get(h, 0) for h in hours]

    fig, ax = plt.subplots(figsize=(14, 6))

    # 막대 그래프
    colors = ['#FF6B6B' if c > max(counts) * 0.7 else
              '#FFA500' if c > max(counts) * 0.4 else
              '#90EE90' for c in counts]

    bars = ax.bar(hours, counts, color=colors, edgecolor='black', linewidth=0.5)

    # 값 표시
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('시간대 (시)', fontsize=12)
    ax.set_ylabel('메시지 수', fontsize=12)
    ax.set_title('시간대별 메시지 활동량', fontsize=16, fontweight='bold')
    ax.set_xticks(hours)
    ax.set_xticklabels([f'{h:02d}' for h in hours])
    ax.grid(axis='y', alpha=0.3)

    # 범례
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF6B6B', label='높음 (>70%)'),
        Patch(facecolor='#FFA500', label='보통 (40-70%)'),
        Patch(facecolor='#90EE90', label='낮음 (<40%)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ 저장: {output_file}")

def create_top_days_chart(stats, output_file, top_n=10):
    """가장 활발한 날 TOP N"""
    print(f"🎨 가장 활발한 날 TOP {top_n} 차트 생성 중...")

    top_days = stats['daily_counts'].most_common(top_n)
    dates = [d[0] for d in top_days]
    counts = [d[1] for d in top_days]

    # 감정 데이터
    positive = [stats['daily_sentiment'][d]['positive'] for d in dates]
    negative = [stats['daily_sentiment'][d]['negative'] for d in dates]
    neutral = [stats['daily_sentiment'][d]['neutral'] for d in dates]

    fig, ax = plt.subplots(figsize=(14, 8))

    x = range(len(dates))
    width = 0.8

    # 스택 막대 그래프
    p1 = ax.bar(x, positive, width, label='긍정 😊', color='#90EE90')
    p2 = ax.bar(x, negative, width, bottom=positive, label='부정 😢', color='#FFB6C1')
    p3 = ax.bar(x, neutral, width, bottom=[p+n for p,n in zip(positive, negative)],
               label='중립 😐', color='#B0C4DE')

    # 총 개수 표시
    for i, (date, count) in enumerate(zip(dates, counts)):
        ax.text(i, count + 5, f'{count}개', ha='center', va='bottom',
               fontweight='bold', fontsize=10)

    ax.set_xlabel('날짜', fontsize=12)
    ax.set_ylabel('메시지 수', fontsize=12)
    ax.set_title(f'가장 활발했던 날 TOP {top_n}', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ 저장: {output_file}")

def main():
    print("=" * 70)
    print("🎨 카카오톡 감정 분석 시각화")
    print("=" * 70)

    # 데이터 파일 (전체 데이터)
    json_file = "full_kakaotalk_analysis_data.json"
    output_dir = "visualizations_full"

    # 출력 디렉토리 생성
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 디렉토리 생성: {output_dir}")

    # 데이터 로드
    data = load_analysis_data(json_file)

    # 통계 계산
    stats = prepare_statistics(data)

    print(f"\n📊 시각화 생성 시작...")

    # 1. 감정 분포 파이 차트
    create_sentiment_pie_chart(stats, f"{output_dir}/sentiment_distribution.png")

    # 2. 발신자별 감정 분포
    create_sender_bar_chart(stats, f"{output_dir}/sender_sentiment.png")

    # 3. 날짜별 활동 추이
    create_daily_activity_chart(stats, f"{output_dir}/daily_activity.png")

    # 4. 시간대별 히트맵
    create_hourly_heatmap(stats, f"{output_dir}/hourly_heatmap.png")

    # 5. TOP 활발한 날
    create_top_days_chart(stats, f"{output_dir}/top_active_days.png")

    print("\n" + "=" * 70)
    print("✅ 시각화 완료!")
    print(f"📁 출력 폴더: {output_dir}/")
    print("=" * 70)

if __name__ == "__main__":
    main()
