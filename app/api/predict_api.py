from app.utils.predict_data_loader import load_parking_data
from app.utils.prediction import *
from flask import Blueprint, request, jsonify
import pandas as pd

prediction_bp = Blueprint('prediction_api', __name__, url_prefix='/predict')

# 停車場資訊表
parking_lots_data = [
    {"carpark_id": "001", "carpark_name": "府前廣場地下停車場"},
    {"carpark_id": "002", "carpark_name": "松壽廣場地下停車場"},
    {"carpark_id": "003", "carpark_name": "臺北市災害應變中心地下停車場"},
    {"carpark_id": "005", "carpark_name": "立農公園地下停車場"},
    {"carpark_id": "007", "carpark_name": "萬華國中地下停車場"},
    {"carpark_id": "014", "carpark_name": "興雅國中地下停車場"},
    {"carpark_id": "018", "carpark_name": "洛陽綜合立體停車場"},
    {"carpark_id": "028", "carpark_name": "松山高中地下停車場"},
    {"carpark_id": "030", "carpark_name": "大稻埕公園地下停車場"},
]

@prediction_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's prediction API"})

# 提供可預測的停車場清單
@prediction_bp.route('/list', methods=['GET'])
def get_parking_list():
    return jsonify({"parking_lots": parking_lots_data})

# 車位預測 API

# 預先載入資料與模型（如有 cache 可優化）
df = load_parking_data()
models = train_models_by_parking_lot(df)

# 更新資料與模型
@prediction_bp.route("/update", methods=['GET'])
def update():
    df = load_parking_data()
    models = train_models_by_parking_lot(df)
    return models 

@prediction_bp.route("/predict", methods=["GET"])
def predict():
    carpark_id = request.args.get("carpark_id")
    date_str = request.args.get("date")  # 格式：YYYY-MM-DD HH:mm:ss
    
    if not carpark_id or not date_str:
        return jsonify({"error": "請提供 carpark_id 與 date 參數"}), 400

    try:
        date = pd.to_datetime(date_str)
    except Exception as e:
        return jsonify({"error": f"日期格式錯誤：{e}"}), 400

    # 預測
    result = predict_availability(models, carpark_id, date_str)
    if result is None:
        return jsonify({"error": f"找不到 {carpark_id} 的模型"}), 404

    # 查找停車場名稱
    carpark_name = next(
        (p["carpark_name"] for p in parking_lots_data if p["carpark_id"] == carpark_id),
        carpark_id  # fallback 用 id
    )

    return jsonify({
        "carpark_id": carpark_id,
        "carpark_name": carpark_name,
        "requested_time": date_str,
        "predicted_availability": int(result["yhat"])
    })
