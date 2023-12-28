import os

from flask import (Blueprint, current_app, flash, render_template, request,
                   url_for)
from flask.views import View
from werkzeug.utils import redirect, secure_filename

from reels_app.main.utils import delete_files
from reels_app.pdf.utils import split

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """Render the index/home page."""
    if request.method == 'POST':

        delete_files('csvs')
        delete_files('pdfs')
        delete_files('uploads/credits')
        delete_files('uploads/files')
        delete_files('uploads/genres')
        delete_files('uploads/invoices')
        delete_files('uploads/photos')
        delete_files('uploads/pdfs')
        delete_files('uploads/purchase_order')
        delete_files('uploads/spreadsheets')

        flash('Files successfully deleted', 'success')
        return redirect(url_for('main.index'))

    return render_template('index.html')


class UploadView(View):
    methods = ['GET', 'POST']

    def __init__(self):
        self.upload_folder = current_app.config['UPLOAD_FOLDER']

    def dispatch_request(self, file_type, function):
        if request.method == 'POST':
            for uploaded_file in request.files.getlist('file'):
                if uploaded_file.filename == '':
                    flash('No file selected', 'warning')
                    return redirect(request.url)
                else:
                    secured_uploaded_file = secure_filename(
                        uploaded_file.filename)
                    uploaded_file.save(os.path.join(
                        self.upload_folder,
                        secured_uploaded_file
                    ))

            flash('File successfully uploaded', 'success')

            if function == 'box-office-report':
                split(self.upload_folder)

            return redirect(url_for('main.index'))
        else:
            # the page title is the function without dashes and title cased
            return render_template('/upload/upload.html',
                                   file_type=file_type, function=function,
                                   title=function.replace('-', ' ').title())
