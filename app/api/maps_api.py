from flask import Blueprint, jsonify

map_bp = Blueprint('maps_api', __name__, url_prefix='/maps')

@map_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's maps API"})
