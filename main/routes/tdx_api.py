from flask import Blueprint, jsonify

tdx_bp = Blueprint('tdx_api', __name__)

@tdx_bp.route('/api/tdx', methods=['GET'])
def get_parking():
    return jsonify({"message": "it's tdx API"}), 
