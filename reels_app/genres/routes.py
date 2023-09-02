import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, send_file, url_for)
from werkzeug.utils import secure_filename

from reels_app.genres.utils import get_genres

genre = Blueprint('genre', __name__)


@genre.route('/upload-genre-list', methods=['GET', 'POST'])
def upload_genre_list():
    """Upload an .xlsx file with a list of films and their IMDB IDs."""
    if request.method == 'POST':
        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No file selected', 'warning')
                return redirect(request.url)
            else:
                secure_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['GENRE_FOLDER'],
                    secure_uploaded_file
                ))
        flash('Genre list successfully uploaded', 'success')

        get_genres(current_app.config['GENRE_FOLDER'])

        return redirect(url_for('genre.download_genres'))

    return render_template('upload/upload-genre-list.html',
                           title='Genre List')


@genre.route('/download-genres', methods=['GET', 'POST'])
def download_genres():
    """Download the uploaded list, now with the genres and trailer URL."""
    files = os.listdir(current_app.config['GENRE_FOLDER'])

    base_path = pathlib.Path(current_app.config['GENRE_FOLDER'])

    if request.method == 'POST':
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for item in base_path.iterdir():
                z.write(item, os.path.basename(item))
        data.seek(0)

        return send_file(data, mimetype='applicatioin/zip',
                         as_attachment=True,
                         download_name='genres.zip')

    return render_template('download/download-files.html', files=files,
                           file_type='XLSX', title='Download Genres')
