from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from api.fgi_cnn import fetch_fng_history
from api.gen_ui import generate_latest_gauge
from api.gen_graph import generate_latest_graph
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI(title="Fear & Greed Index API", description="CNN Fear & Greed Index 데이터를 제공하는 API")

@app.get("/")
def read_root():
    return {"message": "Fear & Greed Index API에 오신 것을 환영합니다!"}

@app.get("/fear-greed-history", response_model=List[Dict[str, Any]])
def get_fear_greed_history(days: int = Query(default=90, ge=1, le=365, description="조회할 일수 (1-365일)")):
    """
    CNN Fear & Greed Index 히스토리 데이터를 반환합니다.
    
    Args:
        days: 조회할 일수 (기본값: 90일, 최대: 365일)
    
    Returns:
        List[Dict]: 날짜별 Fear & Greed Index 데이터
    """
    try:
        data = fetch_fng_history(days)
        return data
    except Exception as e:
        return {"error": f"데이터 조회 중 오류가 발생했습니다: {str(e)}"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/gauge")
def get_fear_greed_gauge():
    """
    최신 Fear & Greed Index 계기판 이미지를 생성하여 반환합니다.
    
    Returns:
        FileResponse: 생성된 계기판 이미지 파일
    """
    try:
        image_path = generate_latest_gauge()
        if image_path:
            return FileResponse(image_path, media_type="image/png")
        else:
            return {"error": "계기판 생성에 실패했습니다."}
    except Exception as e:
        return {"error": f"계기판 생성 중 오류가 발생했습니다: {str(e)}"}

@app.get("/graph")
def get_fear_greed_graph(days: int = Query(default=90, ge=1, le=365, description="조회할 일수 (1-365일)")):
    """
    Fear & Greed Index 라인 그래프를 생성하여 반환합니다.
    
    Args:
        days: 조회할 일수 (기본값: 90일, 최대: 365일)
    
    Returns:
        FileResponse: 생성된 그래프 이미지 파일
    """
    try:
        image_path = generate_latest_graph(days)
        if image_path:
            return FileResponse(image_path, media_type="image/png")
        else:
            return {"error": "그래프 생성에 실패했습니다."}
    except Exception as e:
        return {"error": f"그래프 생성 중 오류가 발생했습니다: {str(e)}"}

@app.get("/score")
def get_latest_score():
    """
    최신 Fear & Greed Index 점수와 상태를 반환합니다.
    
    Returns:
        Dict: 최신 점수, 상태, 날짜 정보
    """
    try:
        data = fetch_fng_history(1)  # 최신 1일 데이터만 가져오기
        if data:
            latest = data[-1]
            return {
                "score": latest['value'],
                "status": latest['status'],
                "date": latest['date'],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {"error": "데이터를 가져올 수 없습니다."}
    except Exception as e:
        return {"error": f"점수 조회 중 오류가 발생했습니다: {str(e)}"}

@app.get("/score-history")
def get_score_history(days: int = Query(default=90, ge=1, le=365, description="조회할 일수 (1-365일)")):
    """
    Fear & Greed Index 점수 히스토리를 반환합니다.
    
    Args:
        days: 조회할 일수 (기본값: 90일, 최대: 365일)
    
    Returns:
        List[Dict]: 날짜별 점수 데이터
    """
    try:
        data = fetch_fng_history(days)
        if data:
            return {
                "history": data,
                "count": len(data),
                "date_range": {
                    "start": data[0]['date'],
                    "end": data[-1]['date']
                }
            }
        else:
            return {"error": "데이터를 가져올 수 없습니다."}
    except Exception as e:
        return {"error": f"점수 히스토리 조회 중 오류가 발생했습니다: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
