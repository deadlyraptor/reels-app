import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_file, url_for)
from werkzeug.utils import secure_filename

from reels_app.credit.utils import get_credits

credit = Blueprint('credit', __name__)


@credit.route('/upload-credits-list', methods=['GET', 'POST'])
def upload_credits_list():
    """Upload an .xlsx file with a list of films and their IMDB IDs."""
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

        get_credits(current_app.config['CREDITS_FOLDER'])

        return redirect(url_for('credit.download_credits'))

    return render_template('upload_credits_list.html', title='Credits List')


@credit.route('/download-credits', methods=['GET', 'POST'])
def download_credits():
    """Download a .docx file with film credits."""
    files = os.listdir(current_app.config['CREDITS_FOLDER'])

    base_path = pathlib.Path(current_app.config['CREDITS_FOLDER'])

    if request.method == 'POST':
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for item in base_path.iterdir():
                # the download folder still has the .xlsx file so the following
                # code excludes it from the download
                if item.name[-4:] == 'docx':
                    z.write(item, os.path.basename(item))
        data.seek(0)

        return send_file(data, mimetype='application/zip',
                         as_attachment=True,
                         download_name='credits.zip')

    return render_template('download-files.html', files=files,
                           file_type='DOCX', title='Download Credits')
