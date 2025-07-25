import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timezone, timedelta
import numpy as np
from api.fgi_cnn import fetch_fng_history
from PIL import Image

# 그래프 스타일 설정
plt.style.use('dark_background')

KST = timezone(timedelta(hours=9))

def create_fear_greed_graph(days: int = 90, save_path: str = "gen_data/fear_greed_graph.png"):
    """
    Fear & Greed Index 라인 그래프 생성
    
    Args:
        days: 조회할 일수 (기본값: 90일)
        save_path: 저장할 파일 경로
    
    Returns:
        str: 생성된 이미지 파일 경로
    """
    try:
        # 데이터 가져오기
        data = fetch_fng_history(days)
        
        if not data:
            raise Exception("데이터를 가져올 수 없습니다.")
        
        # 날짜와 값 분리
        dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in data]
        values = [item['value'] for item in data]
        
        # 그래프 생성
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_position([0, 0, 1, 1])
        
        # 배경을 검은색으로 설정
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        
        # 라인 그래프 그리기
        line_color = '#00BFFF'  # 하늘색/청록색
        ax.plot(dates, values, color=line_color, linewidth=2.5, alpha=0.9)
        
        # Y축 설정 (0-100 범위)
        ax.set_ylim(0, 100)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.set_yticklabels(['0', '25', '50', '75', '100'], color='white', fontsize=16)
        
        # X축 설정 (날짜)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))  # 15일마다 표시
        ax.tick_params(axis='x', colors='white', labelsize=14, rotation=0)
        
        # 격자 설정
        ax.grid(True, alpha=0.2, color='white', linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # 축 레이블 제거 (깔끔한 디자인)
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        # 제목 설정 제거
        # title_text = "Fear & Greed Index"
        # subtitle_text = f"(Last {days} days)"
        # ax.text(0.5, 0.95, title_text, transform=ax.transAxes, 
        #         fontsize=20, fontweight='bold', color='white', 
        #         ha='center', va='top')
        # ax.text(0.5, 0.90, subtitle_text, transform=ax.transAxes, 
        #         fontsize=14, color='#CCCCCC', 
        #         ha='center', va='top')
        # last_updated 변수 선언 추가
        last_updated = datetime.now(KST).strftime("Last updated: %Y-%m-%d %H:%M")
        # 우측 상단에 last updated
        ax.text(0.99, 0.99, last_updated, transform=ax.transAxes,
                fontsize=18, color='#CCCCCC', ha='right', va='top')
        
        # 축 테두리 색상 설정
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['left'].set_linewidth(0.5)
        
        # 레이아웃 조정
        plt.tight_layout()
        plt.savefig(save_path, facecolor='black', bbox_inches='tight', dpi=300)
        plt.close()
        # Pillow로 다운사이징
        img = Image.open(save_path)
        img = img.resize((300, 200), Image.LANCZOS)
        img.save(save_path)
        return save_path
        
    except Exception as e:
        print(f"그래프 생성 중 오류 발생: {str(e)}")
        return None

def generate_latest_graph(days: int = 90, save_path: str = "gen_data/fear_greed_graph.png"):
    """
    최신 Fear & Greed Index 데이터로 그래프 생성
    
    Args:
        days: 조회할 일수 (기본값: 90일)
        save_path: 저장할 파일 경로
    
    Returns:
        str: 생성된 이미지 파일 경로
    """
    return create_fear_greed_graph(days, save_path)

if __name__ == "__main__":
    # 90일간 그래프 생성
    result = generate_latest_graph(90)
    if result:
        print(f"그래프가 생성되었습니다: {result}")
    else:
        print("그래프 생성에 실패했습니다.")
