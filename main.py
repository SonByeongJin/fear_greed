from fastapi import FastAPI, Query
from api.fgi_cnn import fetch_fng_history
from typing import List, Dict, Any

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
