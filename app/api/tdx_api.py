from flask import request, Response, Blueprint, jsonify
import requests , json , os
from flask import jsonify
from app.utils.geocode_utils import get_coords_from_place
from flask import request , Response 
import requests , json 

tdx_bp = Blueprint('tdx_api', __name__, url_prefix='/tdx')

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

@tdx_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's tdx API"})

# === TDX Token ===
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
'''
    if response.status_code != 200:
        print("[ERROR] Token 取得失敗:", response.status_code, response.text)
        
    return response.json().get("access_token")

@tdx_bp.route("/parking_by_place", methods=["GET"])
def get_parking_by_place():
    place = request.args.get("place")
    
    if not place:
        return jsonify({"error": "請提供 place 參數"}), 400

    # 使用 utils 裡的共用函式轉換地址成經緯度
    coords, error = get_coords_from_place(place)
    if error:
        return jsonify({"error": error}), 404
    print(coords)
    lat, lon = coords

    # 將經緯度轉成字串形式，模擬原本 request.args 的參數
    request.args = request.args.copy()
    request.args = request.args.to_dict()
    request.args["lat"] = str(lat)
    request.args["lon"] = str(lon)

    # 重用原有邏輯（呼叫 get_parking_data）
    return get_parking_data()
'''

# === 經緯度轉城市 ===
def get_tdx_city_from_coords(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {"User-Agent": "tdx-parking-service"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        city_name = data.get("address", {}).get("city", "")
        city_map = {
            "臺北市": "Taipei", "台北市": "Taipei",
            "桃園市": "Taoyuan", "臺中市": "Taichung", "台中市": "Taichung",
            "臺南市": "Tainan", "台南市": "Tainan", "高雄市": "Kaohsiung",
            "基隆市": "Keelung", "彰化縣": "ChanghuaCounty", "雲林縣": "YunlinCounty",
            "屏東縣": "PingtungCounty", "宜蘭縣": "YilanCounty", "花蓮縣": "HualienCounty",
            "金門縣": "KinmenCounty"
        }
        return city_map.get(city_name, "")
    return ""

@tdx_bp.route("/parking", methods=["GET"])
def get_parking_data():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    radius = int(request.args.get('radius', 500))

    if not lat or not lon:
        return jsonify({"error": "請提供經緯度 lat 與 lon"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "lat 與 lon 必須為數字"}), 400

    token = get_tdx_token(
        client_id="sssun-09d597db-5ec8-446e",
        client_secret="8ffe4bd6-dc2e-40e1-8f9e-2c5d62e13ab1"
    )
    headers = {"Authorization": f"Bearer {token}"}
    city = get_tdx_city_from_coords(lat, lon)
    if not city:
        return jsonify({"error": "無法辨識城市"}), 500

    # 查詢附近停車場
    nearby_url = f"https://tdx.transportdata.tw/api/advanced/v1/Parking/OffStreet/CarPark/NearBy?" \
                 f"%24spatialFilter=nearby({lat},{lon},{radius})&%24format=JSON"
    nearby_resp = requests.get(nearby_url, headers=headers)
    nearby_data = nearby_resp.json() if nearby_resp.status_code == 200 else []

    # 查詢剩餘空位
    avail_url = f"https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/{city}?%24format=JSON"
    avail_resp = requests.get(avail_url, headers=headers)
    avail_data = avail_resp.json().get("ParkingAvailabilities", []) if avail_resp.status_code == 200 else []
    availability_map = {a["CarParkName"]["Zh_tw"]: a for a in avail_data}

    result = []
    for p in nearby_data:
        name = p.get("CarParkName", {}).get("Zh_tw", "未知")
        lat = p.get("CarParkPosition", {}).get("PositionLat")
        lon = p.get("CarParkPosition", {}).get("PositionLon")
        fare = p.get("FareDescription", "無費率資料")
        match = availability_map.get(name, {})
        available = match.get("AvailableSpaces", 0)

        result.append({
            "name": name,
            "available_spaces": available,
            "price": fare,
            "lat": str(lat),
            "lon": str(lon)
        })

    #return jsonify({"parking_lots": result})
    return Response(
        json.dumps({"parking_lots": result}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )
