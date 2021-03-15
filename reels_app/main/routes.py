import os

from flask import Blueprint, request, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """Render the index/home page."""
    if request.method == 'POST':
        for item in os.listdir('csvs'):
            os.remove(os.path.join('csvs', item))

        for item in os.listdir('uploads/photos'):
            os.remove(os.path.join('uploads/photos', item))

        for item in os.listdir('uploads/spreadsheets'):
            os.remove(os.path.join('uploads/spreadsheets', item))

        return redirect(url_for('main.index'))

    return render_template('index.html', title='Home')
