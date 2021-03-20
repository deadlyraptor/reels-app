import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash,
                   redirect, request, render_template, send_file)
from flask.helpers import url_for
from werkzeug.utils import secure_filename

from xlrd import XLRDError

from .spready import spready

spreadchimp = Blueprint('spreadchimp', __name__)


@spreadchimp.route('/upload-spreadsheet', methods=['GET', 'POST'])
def upload_spreadsheet():
    if request.method == 'POST':

        # upload the spreadsheet
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)
        else:
            secured_uploaded_file = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(
                current_app.config['SPREADSHEET_FOLDER'],
                secured_uploaded_file))

        # creates the CSV files
        try:
            spready(current_app.config['SPREADSHEET_FOLDER'])
        except XLRDError:
            flash('Unsupported file type. Spreadsheet must be .xls, not xlsx.',
                  'warning')
            return redirect(url_for('main.index'))

        return redirect(url_for('spreadchimp.download_csvs'))

    return render_template('upload-spreadsheet.html',
                           title='Upload Spreadsheet')


@spreadchimp.route('/download-csvs', methods=['GET', 'POST'])
def download_csvs():
    files = os.listdir('csvs')

    base_path = pathlib.Path('csvs')

    if request.method == 'POST':
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for item in base_path.iterdir():
                z.write(item, os.path.basename(item))

        data.seek(0)

        return send_file(data, mimetype='application/zip',
                         as_attachment=True,
                         attachment_filename='csv.zip')

    return render_template('download-csvs.html', files=files,
                           title='Download CSVs')
