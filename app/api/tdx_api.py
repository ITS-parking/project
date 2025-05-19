from flask import Blueprint, jsonify

tdx_bp = Blueprint('tdx_api', __name__, url_prefix='/tdx')

@tdx_bp.route('/ping', methods=['GET'])
def pong():
    return jsonify({"message": "it's tdx API"})
