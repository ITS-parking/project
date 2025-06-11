import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import matplotlib

def train_model(data):
    df = data.copy()

    # 處理 Prophet 格式（移除時區、重新命名欄位）
    df["ds"] = df["DataCollectTime"].dt.tz_localize(None)
    df["y"] = df["AvailableSpaces"]

    prophet_df = df[["ds", "y"]]

    # 建立 Prophet 模型並訓練
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)

    # 預測未來 7 天（168 小時）
    future = model.make_future_dataframe(periods=168, freq='H')
    forecast = model.predict(future)

    # 繪圖
    fig = model.plot(forecast)
    plt.title("預測停車場未來車位數")
    plt.xlabel("時間")
    plt.ylabel("可用車位")
    plt.tight_layout()
    plt.grid(True)

    # 儲存成圖片
    plt.savefig("prediction.png")
    print("✅ 圖片已儲存為 prediction.png")

