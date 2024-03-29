import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, redirect,
                   request, render_template, url_for, send_file)
from werkzeug.utils import secure_filename

from reels_app.pdf.pdf import split, rename_deluxe

pdf = Blueprint('pdf', __name__)


@pdf.route('/upload-pdf/<pdf_type>', methods=['GET', 'POST'])
def upload_pdf(pdf_type):
    """Upload a PDF to the server for manipulation.

    pdf_type
        This variable determines the flow of the POST request. If it's set to
        'bor', then the split function is called; if it's set to 'invoice',
        then the rename_deluxe function is called.
    """

    pdf_dir = current_app.config['PDF_FOLDER']

    if request.method == 'POST':

        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No PDF selected', 'warning')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    pdf_dir,
                    secured_uploaded_file))
        flash('PDF successfully uploaded', 'success')

        if pdf_type == 'BOR':
            # split the PDF(s)
            split(pdf_dir)
        elif pdf_type == 'Invoice':
            # rename the PDF(s)
            rename_deluxe(pdf_dir)

        return redirect(url_for('pdf.download_pdfs'))

    return render_template('upload-pdf.html', title=f'Upload {pdf_type}')


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
                         download_name='pdfs.zip')

    return render_template('download-files.html', files=files,
                           file_type='PDFs', title='Download PDFs')
