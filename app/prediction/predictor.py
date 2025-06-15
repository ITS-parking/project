from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

def train_models_by_parking_lot(df):
    models = {}

    for carpark_id, group in df.groupby("CarParkID"):
        prophet_df = group.rename(columns={
            "DataCollectTime": "ds",
            "AvailableSpaces": "y"
        })

        # 移除 timezone 資訊
        prophet_df["ds"] = pd.to_datetime(prophet_df["ds"]).dt.tz_localize(None)

        model = Prophet(daily_seasonality=True)
        model.fit(prophet_df)
        models[carpark_id] = model

    print("✅ 所有模型訓練完畢")
    return models

def predict_availability(models, carpark_id, date_str):
    if carpark_id not in models:
        print(f"❌ 找不到 {carpark_id} 的模型")
        return

    model = models[carpark_id]
    future = model.make_future_dataframe(periods=168, freq='H')  # 7天預測
    forecast = model.predict(future)

    date = pd.to_datetime(date_str)
    forecast["ds"] = pd.to_datetime(forecast["ds"])
    
    nearest_row = forecast.loc[(forecast["ds"] - date).abs().idxmin()]
    print(f"✅ {carpark_id} 在 {date_str} 預測可用車位為：{int(nearest_row['yhat'])}")
    return nearest_row
