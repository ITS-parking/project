from app import create_app
import os
from threading import Timer

app = create_app()

def open_browser():
    os.system("explorer.exe http://127.0.0.1:5000/apidocs/")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)
