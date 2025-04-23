from flask import Flask
from routes import maps_api, tdx_api

app = Flask(__name__)

# 註冊 API Blueprint
app.register_blueprint(maps_api)
app.register_blueprint(tdx_api)

@app.route('/')
def index():
    return "導航系統啟動成功"

if __name__ == '__main__':
    app.run(debug=True)
