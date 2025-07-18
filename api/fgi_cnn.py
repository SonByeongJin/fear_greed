import requests
from datetime import datetime
from api.classify_grade import classify_grade

def convert_x_to_date(x):
    if isinstance(x, str):
        return datetime.strptime(x, "%Y-%m-%d").strftime("%Y-%m-%d")
    elif isinstance(x, (int, float)):
        return datetime.fromtimestamp(x / 1000).strftime("%Y-%m-%d")
    else:
        raise ValueError(f"알 수 없는 날짜 형식: {x}")
    
def deduplicate_by_date(data):
    seen = set()
    result = []
    for item in data:
        if item["x"] not in seen:
            seen.add(item["x"])
            result.append(item)
    return result

def fetch_fng_history():
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"❌ 요청 실패: {resp.status_code}")

    raw = resp.json()
    full_data = raw["fear_and_greed_historical"]["data"]
    deduplicate_data = deduplicate_by_date(full_data)

    last_365 = deduplicate_data[-365:]

    formatted = [
        {
            "date": convert_x_to_date(item["x"]),
            "value": item["y"],
            "status": classify_grade(item["y"])
        }
        for item in last_365
    ]
    return formatted

if __name__ == "__main__":
    import json
    result = fetch_fng_history()
    print(json.dumps(result[-5:], indent=2))
