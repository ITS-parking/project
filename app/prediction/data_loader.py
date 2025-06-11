from pathlib import Path
import json
import pandas as pd

def load_parking_data():
    root = Path(__file__).resolve().parents[2]
    json_path = root / "data_collection" / "output" / "parking_data.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    records = []
    for entry in raw_data:
        timestamp = entry["timestamp"]
        for park in entry["data"]:
            carpark_id = park["CarParkID"]
            data_collect_time = park["DataCollectTime"]
            
            # 取得 SpaceType=1 的 AvailableSpaces
            type1_avail = None
            for avail in park["Availabilities"]:
                if avail["SpaceType"] == 1:
                    type1_avail = avail["AvailableSpaces"]
                    break
            
            if type1_avail is not None:
                records.append({
                    "CarParkID": carpark_id,
                    "DataCollectTime": pd.to_datetime(data_collect_time),
                    "AvailableSpaces": type1_avail
                })

    # 轉換成 DataFrame
    df = pd.DataFrame(records)

    return df
