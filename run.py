from app import create_app
import os
from threading import Timer
import webbrowser

app = create_app()

def open_browser():
    webbrowser.open("explorer.exe http://127.0.0.1:5000/apidocs/")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)

