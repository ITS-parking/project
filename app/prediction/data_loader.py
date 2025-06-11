from pathlib import Path
import json

def load_parking_data():
    root = Path(__file__).resolve().parents[2]
    json_path = root / "data_collection" / "output" / "parking_data.json"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data
