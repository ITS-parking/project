from flask import request, Response, Blueprint, jsonify
import requests , json, jsonify, os

tdx_bp = Blueprint('tdx_api', __name__, url_prefix='/tdx')

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

# === test === 
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
        client_id=APP_ID,
        client_secret=APP_KEY
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
