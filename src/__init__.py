"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Database setup
from src.config import DevelopmentConfig, TestingConfig

db = SQLAlchemy()


def init_app(test=False):
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    if not test:
        app.config.from_object(DevelopmentConfig)  # configure app using the Config class defined in src/config.py
        from src.models import Appartment
        db.init_app(app)  # initialise the database for the app
        with app.app_context():
            db.create_all()
    else:
        app.config.from_object(TestingConfig)  # configure app test config


    with app.app_context():
        from src.routes import api_bp
        app.register_blueprint(api_bp)
        return app