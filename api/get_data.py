import os
import json
from datetime import datetime, timedelta
from api.fgi_cnn import fetch_fng_history

DATA_PATH = "data/score_history.json"


def update_fear_greed_index():
    os.makedirs("data", exist_ok=True)

    history = fetch_fng_history()

    with open("data/score_history.json", "w") as f:
        json.dump(history, f, indent=2)



if __name__ == "__main__":
    update_fear_greed_index()








