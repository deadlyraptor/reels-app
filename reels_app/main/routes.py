from flask import Blueprint, flash, request, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect

from reels_app.main.utils import delete_files

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """Render the index/home page."""
    if request.method == 'POST':

        delete_files('csvs')
        delete_files('pdfs')
        delete_files('uploads/invoices')
        delete_files('uploads/photos')
        delete_files('uploads/pdfs')
        delete_files('uploads/spreadsheets')

        flash('Files successfully deleted', 'success')
        return redirect(url_for('main.index'))

    return render_template('index.html')
