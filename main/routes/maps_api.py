from flask import Blueprint, jsonify

maps_bp = Blueprint('maps_api', __name__)

@maps_bp.route('/api/maps', methods=['GET'])
def get_route():
    return jsonify({"message": "it's maps API"})
