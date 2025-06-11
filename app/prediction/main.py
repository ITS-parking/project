from data_loader import load_parking_data
import pandas as pd

def data():
    data = load_parking_data()
    return data

def available(df):
    # 只保留主欄位與展開的 SpaceType = 1 資訊
    def extract_type_1(avail_list):
        for item in avail_list:
            if item["SpaceType"] == 1:
                return item["AvailableSpaces"], item["NumberOfSpaces"]
        return None, None

    df[["type1_avail", "type1_total"]] = df["Availabilities"].apply(
        lambda x: pd.Series(extract_type_1(x))
    )
    return df

def test(data):
    df = pd.DataFrame(data)
    print("資料筆數：", len(df))    

if __name__ == "__main__":
    data()


    
