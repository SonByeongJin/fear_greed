"""
| 점수 범위    | 상태 (`status`)   |
| ----------- | ---------------- |
| 0 \~ 24     |  `Extreme Fear`  |
| 25 \~ 44    |  `Fear`          |
| 45 \~ 54    |  `Neutral`       |
| 55 \~ 74    |  `Greed`         |
| 75 \~ 100   |  `Extreme Greed` |
"""

def classify_grade(value: float) -> str:
    if value < 25:
        return "Extreme Fear"
    elif value < 45:
        return "Fear"
    elif value < 55:
        return "Neutral"
    elif value < 75:
        return "Greed"
    else:
        return "Extreme Greed"
