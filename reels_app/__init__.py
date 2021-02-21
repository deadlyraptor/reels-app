from flask import Flask

from reels_app.main.routes import main


def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main)

    return None
