import os

from flask import Blueprint, flash, request, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """Render the index/home page."""
    if request.method == 'POST':

        def delete_files(directory):
            for item in os.listdir(directory):
                os.remove(os.path.join(directory, item))

        delete_files('csvs')
        delete_files('pdfs')
        delete_files('uploads/photos')
        delete_files('uploads/spreadsheets')
        delete_files('uploads/pdfs')

        flash('Files deleted successfully', 'success')
        return redirect(url_for('main.index'))

    return render_template('index.html', title='Home')
