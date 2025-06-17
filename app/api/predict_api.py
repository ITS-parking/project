from app.utils.predict_data_loader import load_parking_data
from app.utils.prediction import *
from flask import Blueprint, request, jsonify, current_app
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

# 初始化時預載模型
def init_model():
    df = load_parking_data()
    models = train_models_by_parking_lot(df)
    current_app.config["MODELS_CACHE"] = models
    return models

# 獲取最新模型（避免 None）
def get_models():
    return current_app.config.get("MODELS_CACHE") or init_model()

@prediction_bp.route("/update", methods=['POST'])
def update_models():
    try:
        df = load_parking_data()
        models = train_models_by_parking_lot(df)
        current_app.config["MODELS_CACHE"] = models
        return jsonify({"message": "模型已更新", "model_count": len(models)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@prediction_bp.route("/predict", methods=["GET"])
def predict():
    carpark_id = request.args.get("carpark_id")
    date_str = request.args.get("date")
    
    if not carpark_id or not date_str:
        return jsonify({"error": "請提供 carpark_id 與 date 參數"}), 400

    try:
        date = pd.to_datetime(date_str)
    except Exception as e:
        return jsonify({"error": f"日期格式錯誤：{e}"}), 400

    models = get_models()
    result = predict_availability(models, carpark_id, date_str)
    if result is None:
        return jsonify({"error": f"找不到 {carpark_id} 的模型"}), 404

    carpark_info = next((p for p in parking_lots_data if p["carpark_id"] == carpark_id), None)
    if not carpark_info:
        return jsonify({"error": f"找不到 {carpark_id} 的資訊"}), 404

    total_spaces = carpark_info.get("total_spaces", 500)

    return jsonify({
        "carpark_id": carpark_id,
        "carpark_name": carpark_info["carpark_name"],
        "requested_time": date_str,
        "predicted_availability": int(result["yhat"]),
        "total_spaces": total_spaces
    })
