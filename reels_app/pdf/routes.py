import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, redirect,
                   request, render_template, url_for, send_file)
from werkzeug.utils import secure_filename

from reels_app.pdf.pdf import split

pdf = Blueprint('pdf', __name__)


@pdf.route('/upload-pdf', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':

        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No PDF selected', 'warning')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['PDF_FOLDER'],
                    secured_uploaded_file))
        flash('PDF successfully uploaded', 'success')

        # split the PDF
        split(current_app.config['PDF_FOLDER'])
        return redirect(url_for('pdf.download_pdfs'))

    return render_template('upload-pdf.html', title='Upload BOR')


@pdf.route('/download-pdfs', methods=['GET', 'POST'])
def download_pdfs():
    files = os.listdir('pdfs')

    base_path = pathlib.Path('pdfs')

    if request.method == 'POST':
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for item in base_path.iterdir():
                z.write(item, os.path.basename(item))

        data.seek(0)

        return send_file(data, mimetype='application/zip',
                         as_attachment=True,
                         attachment_filename='pdfs.zip')

    return render_template('download-files.html', files=files,
                           file_type='PDFs', title='Download PDFs')
