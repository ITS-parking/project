from flask import Flask
from flasgger import Swagger
from app.api import register_routes

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app, template_file='../api.yml')
    register_routes(app)

    
    return app