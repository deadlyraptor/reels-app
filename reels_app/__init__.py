from flask import Flask

from reels_app.main.routes import main

from settings import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main)

    return None
