from flask import Flask
from .routes import main  # importe le blueprint défini dans routes.py

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  #  enregistre le blueprint
    return app