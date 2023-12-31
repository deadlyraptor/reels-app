from flask import Flask

# from flask_dropzone import Dropzone

from reels_app.main.routes import main, DownloadView, UploadView
from reels_app.rename.routes import rename
from reels_app.spreadchimp.routes import spreadchimp


from settings import Config

# dropzone = Dropzone()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.add_url_rule('/upload-file/<file_type>/<function>',
                     view_func=UploadView.as_view(
                         name='upload_file'))
    app.add_url_rule('/download-files',
                     view_func=DownloadView.as_view(
                         name='download_files'
                     ))

    register_blueprints(app)
    # dropzone.init_app(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main)
    app.register_blueprint(rename)
    app.register_blueprint(spreadchimp)

    return None
