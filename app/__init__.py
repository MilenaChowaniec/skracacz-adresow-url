"""
Inicjalizacja aplikacji Flask.
Tworzenie i konfiguracja aplikacji.
"""

from flask import Flask
import os
from app.database import db


def create_app(config_overrides=None):
    """Tworzy i konfiguruje aplikacje Flask.

    Returns:
        Flask: skonfigurowana aplikacja.
    """
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "my-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app) # Podlaczenie bazy danych

    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app
