import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, redirect,
                   request, render_template, send_file, send_from_directory,
                   url_for)
from werkzeug.utils import secure_filename

rename = Blueprint('rename', __name__)


@rename.route('/upload-photos', methods=['GET', 'POST'])
def upload_photos():
    if request.method == 'POST':

        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No selected file', 'warning')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['PHOTOS_FOLDER'],
                    secured_uploaded_file))
        flash('File successfully uploaded', 'success')
        return redirect(url_for('rename.rename_photos'))

    return render_template('upload-photos.html', title='Upload Photos')


@rename.route('/rename-photos', methods=['GET', 'POST'])
def rename_photos():
    if request.method == 'POST':
        name = request.form['name'].lower()
        path = current_app.config['PHOTOS_FOLDER']

        if name == '':
            flash('Enter a new base filename', 'warning')
            return redirect(request.url)
        else:
            with os.scandir(path) as directory:
                for number, photo in enumerate(directory, start=1):
                    new_name = f'{name}-still-{str(number).zfill(2)}.{photo.name.split(".")[1]}'  # noqa
                    os.rename(photo, f'{path}/{new_name}')

            flash('Photos successfully renamed', 'success')
            return redirect(url_for('rename.download_photos'))

    return render_template('rename-photos.html', title='Rename Photos')


@rename.route('/uploads/photos/<path:filename>')
def upload(filename):
    return send_from_directory(current_app.config['PHOTOS_FOLDER'], filename)


@rename.route('/download-photos', methods=['GET', 'POST'])
def download_photos():
    files = os.listdir(current_app.config['PHOTOS_FOLDER'])

    base_path = pathlib.Path('uploads/photos')

    if request.method == 'POST':
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for item in base_path.iterdir():
                z.write(item, os.path.basename(item))

        data.seek(0)

        return send_file(data, mimetype='application/zip',
                         as_attachment=True,
                         attachment_filename='photos.zip')

    return render_template('download-photos.html', files=files)
