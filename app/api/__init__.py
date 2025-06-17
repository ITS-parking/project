from app.api.maps_api import map_bp as maps_bp
from app.api.tdx_api import tdx_bp as tdx_bp
from app.api.predict_api import prediction_bp as predictor_bp

def register_routes(app):
    app.register_blueprint(maps_bp)
    app.register_blueprint(tdx_bp)
    app.register_blueprint(predictor_bp)