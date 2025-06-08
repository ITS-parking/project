import requests
import pandas as pd

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

# === 經緯度轉城市（轉成 TDX 用格式） ===
def get_tdx_city_from_coords(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {"User-Agent": "your-app-name"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        city_name = data.get("address", {}).get("city", "")
        print(f"🔍 解析到城市名稱: {city_name}")

        # 限定 TDX 有支援剩餘車位查詢的城市
        city_map = {
            "臺北市": "Taipei",
            "台北市": "Taipei",
            "新北市": "NewTaipei",
            "桃園市": "Taoyuan",
            "臺中市": "Taichung",
            "台中市": "Taichung",
            "臺南市": "Tainan",
            "台南市": "Tainan",
            "彰化縣": "ChanghuaCounty",
            "屏東縣": "PingtungCounty",
            "花蓮縣": "HualienCounty"
        }

        tdx_city = city_map.get(city_name, "")
        if not tdx_city:
            print("⚠️ 此城市不支援剩餘車位查詢")
        else:
            print(f"📍 查詢城市: {tdx_city}")
        return tdx_city
    return ""


# === 憑證與參數設定 ===
# === 憑證與設定 ===
#client_id = REMOVED
#client_secret = REMOVED
client_id = REMOVED 
#REMOVED
client_secret = REMOVED
token = get_tdx_token(client_id, client_secret)
headers = {"Authorization": f"Bearer {token}"}

# === 查詢參數 ===
# === 查詢條件 ===
latitude =     23.7440808322313
longitude = 120.86230454546988
radius = 1000
#city = "Taipei"

# === 判定城市 ===
city = get_tdx_city_from_coords(latitude, longitude)
print("📍 查詢城市:", city)

# === 查詢附近路邊停車格（取得 SectionID） ===
spot_url = f"https://tdx.transportdata.tw/api/basic/v1/Parking/OnStreet/ParkingSpot/NearBy?" \
           f"%24spatialFilter=nearby({latitude}%2C{longitude}%2C{radius})&%24format=JSON"
spot_resp = requests.get(spot_url, headers=headers)
spot_data = spot_resp.json() if spot_resp.status_code == 200 else []
section_ids = list(set([s["SectionID"] for s in spot_data]))
print(f"✅ 共找到 {len(section_ids)} 筆路段 SegmentID")

# === 查詢全市的剩餘資訊與路段基本資料 ===
avail_url = f"https://tdx.transportdata.tw/api/basic/v1/Parking/OnStreet/ParkSegmentAvailability/City/{city}?%24format=JSON"
avail_resp = requests.get(avail_url, headers=headers)
avail_data = avail_resp.json() if avail_resp.status_code == 200 else []
avail_map = {a["SectionID"]: a for a in avail_data}

import json 
# === 查詢該城市的基本路段資訊 ===
info_url = f"https://tdx.transportdata.tw/api/basic/v1/Parking/OnStreet/ParkingSegment/City/{city}?%24format=JSON"
info_resp = requests.get(info_url, headers=headers)
info_data = info_resp.json().get("ParkingSegments", []) if info_resp.status_code == 200 else []
#print(json.dumps(info_resp.json(), indent=2, ensure_ascii=False))

#info_map = {i["SectionID"]: i for i in info_data}
info_map = {i["ParkingSegmentID"]: i for i in info_data}


# === 組合輸出資料 ===
records = []
for sid in section_ids:
    info = info_map.get(sid)
    avail = avail_map.get(sid)
    if not info:
        continue
    records.append({
        "路段ID": sid,
        "名稱": info.get("SectionName", "無名稱"),
        "起訖": f"{info.get('FromRoad', '')} ➜ {info.get('ToRoad', '')}",
        "收費": info.get("ChargeDescription", "無資料"),
        "說明": info.get("Remark", ""),
        "緯度": info.get("PositionLat", "無"),
        "經度": info.get("PositionLon", "無"),
        "總格數": avail.get("TotalSpaces", "無") if avail else "無",
        "剩餘格數": avail.get("AvailableSpaces", "無") if avail else "無"
    })

# === 輸出 CSV ===
df = pd.DataFrame(records)
df.to_csv("roadside_parking_info.csv", index=False, encoding="utf-8-sig")
print("✅ 路邊停車資料已輸出為 roadside_parking_info.csv")
