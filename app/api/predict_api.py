from app.utils.predict_data_loader import load_parking_data
from app.utils.prediction import *
from flask import Blueprint, request, jsonify
import pandas as pd

prediction_bp = Blueprint('prediction_api', __name__, url_prefix='/predict')

@prediction_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's prediction API"})

# 預測車位數 API
@prediction_bp.route("/predict", methods=["GET"])
def predict():
    carpark_id = request.args.get("carpark_id")
    
    # !!! 僅提供未來一周預測
    date_str = request.args.get("date")  # 格式：YYYY-MM-DD HH:mm:ss

    if not carpark_id or not date_str:
        return jsonify({"error": "請提供 carpark_id 與 date 參數"}), 400

    try:
        date = pd.to_datetime(date_str)
    except Exception as e:
        return jsonify({"error": f"日期格式錯誤：{e}"}), 400

    # 載入資料並訓練模型（實務上應 cache）
    df = load_parking_data()
    models = train_models_by_parking_lot(df)

    # 進行預測
    result = predict_availability(models, carpark_id, date_str)
    if result is None:
        return jsonify({"error": f"找不到 {carpark_id} 的模型"}), 404

    return jsonify({
        "carpark_id": carpark_id,
        "requested_time": date_str,
        "predicted_availability": int(result["yhat"])
    })
