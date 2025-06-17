from flask import Flask, render_template
from app.linebot.webhook import linebot_bp
from flasgger import Swagger
from app.api import register_routes

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.register_blueprint(linebot_bp)
    swagger = Swagger(app, template_file='../api.yml')
    register_routes(app)

    @app.route("/preview")
    def preview():
        return render_template("preview.html")
    
    @app.route("/demo")
    def demo():
        return render_template("demo.html")
    
    @app.route("/callback", methods=["POST"])
    def callback():
        return "ok"

    return app