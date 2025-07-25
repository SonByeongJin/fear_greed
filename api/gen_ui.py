import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc, FancyBboxPatch
import numpy as np
from datetime import datetime, timezone, timedelta
from api.fgi_cnn import fetch_fng_history
import matplotlib.font_manager as fm
from PIL import Image

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

KST = timezone(timedelta(hours=9))

def get_status_color(status: str) -> str:
    """상태에 따른 색상 반환"""
    colors = {
        "Extreme Fear": "#FF4444",  # 빨간색
        "Fear": "#FF8844",          # 주황색
        "Neutral": "#FFAA44",       # 노란색
        "Greed": "#44AA44",         # 연두색
        "Extreme Greed": "#44FF44"  # 밝은 초록색
    }
    return colors.get(status, "#FFFFFF")

def get_status_korean(status: str) -> str:
    """영어 상태를 그대로 반환 (한국어 변환 제거)"""
    return status

def create_fear_greed_gauge(value: float, status: str, save_path: str = "gen_data/fear_greed_score.png"):
    """
    Fear & Greed Index 계기판 생성
    
    Args:
        value: Fear & Greed Index 값 (0-100)
        status: 상태 문자열
        save_path: 저장할 파일 경로
    """
    # 그림 크기 설정 (원래대로)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.set_aspect('equal')
    
    # 배경을 검은색으로 설정
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # 축 숨기기
    ax.axis('off')
    
    # 반원형 게이지 그리기
    center = (0, 0)
    radius = 1.0
    
    # 게이지 배경 (회색)
    arc_bg = Arc(center, 2*radius, 2*radius, theta1=0, theta2=180, 
                linewidth=20, color='#333333', alpha=0.3)
    ax.add_patch(arc_bg)
    
    # 색상 그라데이션을 위한 각도 계산 (왼쪽이 빨간색, 오른쪽이 초록색)
    angles = np.linspace(0, 180, 100)
    colors = plt.cm.RdYlGn(np.linspace(1, 0, 100))  # 초록-노랑-빨강 그라데이션 (순서 뒤집기)
    
    # 그라데이션 게이지 그리기 (왼쪽부터 오른쪽으로)
    for i in range(len(angles)-1):
        arc = Arc(center, 2*radius, 2*radius, 
                 theta1=angles[i], theta2=angles[i+1],
                 linewidth=20, color=colors[i])
        ax.add_patch(arc)
    
    # 현재 값에 따른 바늘 위치 계산 (0-100을 180-0도로 변환하여 왼쪽이 작은 값, 오른쪽이 큰 값)
    needle_angle = 180 - (value / 100) * 180
    
    # 바늘 그리기
    needle_length = 0.8
    needle_x = needle_length * np.cos(np.radians(needle_angle))
    needle_y = needle_length * np.sin(np.radians(needle_angle))
    
    # 바늘 선
    ax.plot([0, needle_x], [0, needle_y], color='white', linewidth=8, solid_capstyle='round')
    
    # 바늘 끝 원
    circle = plt.Circle((needle_x, needle_y), 0.05, color='white', zorder=10)
    ax.add_patch(circle)
    
    # 중심점
    center_circle = plt.Circle((0, 0), 0.08, color='white', zorder=10)
    ax.add_patch(center_circle)
    
    # 값 표시
    ax.text(0, -0.3, f"{int(value)}", fontsize=44, fontweight='bold', 
            color='white', ha='center', va='center')
    
    # 상태 텍스트
    status_color = get_status_color(status)
    korean_status = get_status_korean(status)
    ax.text(0, -0.5, korean_status, fontsize=35, fontweight='bold',
            color=status_color, ha='center', va='center')
    
    # 현재 시간 표시
    current_time = datetime.now(KST).strftime("%Y. %m. %d. %p %I:%M")
    ax.text(0, -0.7, f"Last updated: {current_time}", fontsize=19,
            color='#888888', ha='center', va='center')
    
    # 제목 제거
    # ax.text(0, 1.1, "Fear & Greed Index", fontsize=20, fontweight='bold',
    #         color='white', ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(save_path, facecolor='black', bbox_inches='tight', dpi=300)
    plt.close()
    # Pillow로 다운사이징
    img = Image.open(save_path)
    img = img.resize((200, 200), Image.LANCZOS)
    img.save(save_path)
    return save_path

def generate_latest_gauge(days: int = 1, save_path: str = "gen_data/fear_greed_score.png"):
    """
    최신 Fear & Greed Index 데이터를 가져와서 계기판 생성
    
    Args:
        days: 조회할 일수 (기본값: 1일)
        save_path: 저장할 파일 경로
    
    Returns:
        str: 생성된 이미지 파일 경로
    """
    try:
        # 최신 데이터 가져오기
        data = fetch_fng_history(days)
        
        if not data:
            raise Exception("데이터를 가져올 수 없습니다.")
        
        # 최신 데이터 (마지막 항목)
        latest = data[-1]
        value = latest['value']
        status = latest['status']
        
        # 계기판 생성
        return create_fear_greed_gauge(value, status, save_path)
        
    except Exception as e:
        print(f"계기판 생성 중 오류 발생: {str(e)}")
        return None

if __name__ == "__main__":
    # 최신 계기판 생성
    result = generate_latest_gauge()
    if result:
        print(f"계기판이 생성되었습니다: {result}")
    else:
        print("계기판 생성에 실패했습니다.")
