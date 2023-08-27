import os

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from werkzeug.utils import secure_filename
import tmdbsimple as tmdb

from reels_app.credit.utils import build_film_list

credit = Blueprint('credit', __name__)


@credit.route('/upload-credits-list', methods=['GET', 'POST'])
def upload_credits_list():
    """Upload an .xlsx file with a list of films to get credits for."""

    if request.method == 'POST':
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No file selected', 'warning')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['CREDITS_FOLDER'],
                    secured_uploaded_file
                ))
        flash('Credit list successfully uploaded', 'success')

        build_film_list(current_app.config['CREDITS_FOLDER'])

        return redirect(url_for('credit.upload_credits_list')
                        )
    return render_template('upload_credits_list.html', title='Credits List')
