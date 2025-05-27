from flask import Flask
from .routes import main  # Importamos las rutas definidas en routes.py

def create_app():
    app = Flask(__name__)   # Creamos la app
    app.register_blueprint(main)  # Registramos las rutas (blueprint)
    return app
