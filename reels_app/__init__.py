from flask import Flask

from flask_dropzone import Dropzone

from reels_app.main.routes import main
from reels_app.credit.routes import credit
from reels_app.pdf.routes import pdf
from reels_app.po.routes import po
from reels_app.rename.routes import rename
from reels_app.spreadchimp.routes import spreadchimp

from settings import Config

dropzone = Dropzone()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_blueprints(app)
    dropzone.init_app(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main)
    app.register_blueprint(credit)
    app.register_blueprint(pdf)
    app.register_blueprint(po)
    app.register_blueprint(rename)
    app.register_blueprint(spreadchimp)

    return None
