from data_loader import load_parking_data
from predictor import train_model

def test(data):
    print("資料筆數：", len(data))    
    print(data.head())

if __name__ == "__main__":
    data = load_parking_data()
    print(type(data))  # 確認是 DataFrame
    test(data)
    train_model(data)  # 直接用 load_parking_data 回傳的 DataFrame 訓練
