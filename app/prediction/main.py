from data_loader import load_parking_data
from predictor import *

if __name__ == "__main__":
    df = load_parking_data()
    models = train_models_by_parking_lot(df)

    # 測試：查詢 001 停車場在 2025-06-14 15:00 的預測
    predict_availability(models, "030", "2025-06-17 19:00")
