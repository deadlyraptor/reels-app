import os

from flask import (Blueprint, current_app, flash, redirect,
                   request, render_template, url_for)
from werkzeug.utils import secure_filename

from PyPDF2 import PdfFileReader, PdfFileWriter

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
        return redirect(url_for('pdf.split_pdf'))

    return render_template('upload-pdf.html', title='Upload PDF')
