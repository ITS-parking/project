from flask import Blueprint, jsonify, request, Response
import requests
import json
from app.utils.geocode_utils import get_coords_from_place

map_bp = Blueprint('maps_api', __name__, url_prefix='/maps')

@map_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's maps API"})

@map_bp.route("/geocode", methods=["GET"])
def geocode():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "請提供 place 參數"}), 400

    coords, error = get_coords_from_place(place)
    if error:
        return jsonify({"error": error}), 404

    lat, lon = coords
    return jsonify({
        "place": place,
        "lat": lat,
        "lon": lon
    })
