# translation.py

from app import app
from flask import Flask, render_template
from app.routes import home_route_blueprint
from app.translate import upload_route_blueprint
from app.whiper import whisper_route_blueprint
app = Flask(__name__)

app.register_blueprint(home_route_blueprint)
app.register_blueprint(upload_route_blueprint)
app.register_blueprint(whisper_route_blueprint)

if __name__ == "__main__":
    app.run()
