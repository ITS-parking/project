from flask import Blueprint, jsonify, request, Response
import requests
import json

map_bp = Blueprint('maps_api', __name__, url_prefix='/maps')

@map_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's maps API"})

@map_bp.route("/geocode", methods=["GET"])
def geocode():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "請提供 place 參數"}), 400

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "ITS-Parking-Info"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            return jsonify({"error": "查無資料"}), 404

        return Response(
            json.dumps({
                "place": place,
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
