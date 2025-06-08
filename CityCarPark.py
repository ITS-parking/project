import requests

# === 取得 TDX Token ===
def get_tdx_token(client_id, client_secret):
    url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

import requests ,json 

def get_tdx_city_from_coords(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {"User-Agent": "your-app-name"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        #print(json.dumps(data.get("address", {}), indent=2, ensure_ascii=False))

        city_name = data.get("address", {}).get("city", "")
        print(city_name)
        # 建立 TDX 支援的城市英文對照
        city_map = {
            "臺北市": "Taipei",
            "台北市": "Taipei",
            "桃園市": "Taoyuan",
            "臺中市": "Taichung",
            "台中市": "Taichung",
            "臺南市": "Tainan",
            "台南市": "Tainan",
            "高雄市": "Kaohsiung",
            "基隆市": "Keelung",
            "彰化縣": "ChanghuaCounty",
            "雲林縣": "YunlinCounty",
            "屏東縣": "PingtungCounty",
            "宜蘭縣": "YilanCounty",
            "花蓮縣": "HualienCounty",
            "金門縣": "KinmenCounty"
        }
        return city_map.get(city_name, "")  # 沒對應就回空字串或預設城市
    return ""
 

# === 憑證與設定 ===
#client_id = REMOVED
#client_secret = REMOVED
client_id = REMOVED 
#REMOVED
client_secret = REMOVED
token = get_tdx_token(client_id, client_secret)
headers = {"Authorization": f"Bearer {token}"}

# === 查詢條件 ===
latitude =    25.043334291331682
longitude = 121.55633620331601
radius = 1000
#city = "Taipei"

# ==  轉換程式 ==== 

city = get_tdx_city_from_coords(latitude, longitude)

print(city) 

# === 查詢附近停車場 ===
nearby_url = f"https://tdx.transportdata.tw/api/advanced/v1/Parking/OffStreet/CarPark/NearBy?" \
             f"%24spatialFilter=nearby%28{latitude}%2C%20{longitude}%2C%20{radius}%29&%24format=JSON"
nearby_resp = requests.get(nearby_url, headers=headers)
nearby_data = nearby_resp.json() if nearby_resp.status_code == 200 else []

# === 查詢剩餘空位資料 ===
avail_url = f"https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/{city}?%24format=JSON"
avail_resp = requests.get(avail_url, headers=headers)
avail_data = avail_resp.json().get("ParkingAvailabilities", []) if avail_resp.status_code == 200 else []

# === 建立名稱對照表 ===
availability_map = {
    a["CarParkName"]["Zh_tw"]: a for a in avail_data
}

import pandas as pd

# === 準備儲存資料的列表 ===
records = []

# === 整合兩筆資料 ===
for p in nearby_data:
    name = p.get("CarParkName", {}).get("Zh_tw", "無名稱")
    address = p.get("Address", "無地址")
    fare = p.get("FareDescription", "無費率資料")
    lat = p.get("CarParkPosition", {}).get("PositionLat", "無緯度")
    lon = p.get("CarParkPosition", {}).get("PositionLon", "無經度")

    avail = availability_map.get(name)
    total = avail.get("TotalSpaces", "無資料") if avail else "無資料"
    available = avail.get("AvailableSpaces", "無資料") if avail else "無資料"
    status = avail.get("ServiceStatus", "未知") if avail else "無資料"

    #print(f"🚗 名稱: {name}")
    #print(f"📍 地址: {address}")
    #print(f"💰 計費: {fare}")
    #print(f"🌐 座標: ({lat}, {lon})")
    #print(f"📦 總車位: {total} | 🈳 剩餘: {available} | 狀態: {status}")
    #print("-" * 60)

    # 加入到列表
    records.append({
        "名稱": name,
        "地址": address,
        "計費": fare,
        "緯度": lat,
        "經度": lon,
        "總車位": total,
        "剩餘空位": available,
        "狀態": status
    })

# === 轉為 DataFrame 並輸出為 CSV 檔案 ===
df = pd.DataFrame(records)
df.to_csv("parking_info.csv", index=False, encoding="utf-8-sig")  # UTF-8 with BOM for Excel 兼容
print("✅ 停車場資料已輸出為 parking_info.csv")

