import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, render_template, request,
                   send_file, url_for)
from flask.views import View
from werkzeug.utils import redirect, secure_filename

from reels_app.credit.utils import get_credits
from reels_app.genres.utils import write_genre_trailer
from reels_app.main.utils import delete_files
from reels_app.pdf.utils import rename_deluxe_invoices, split_box_office_report
from reels_app.po.utils import prep_po, parse_deluxe_invoice

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """Render the index/home page."""
    if request.method == 'POST':

        delete_files('csvs')
        delete_files('pdfs')
        delete_files('downloads')
        delete_files('uploads/files')
        delete_files('uploads/photos')
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
                split_box_office_report(self.upload_folder)
                return redirect(url_for('download_files'))
            elif function == 'rename-deluxe-invoices':
                rename_deluxe_invoices(self.upload_folder)
                return redirect(url_for('download_files'))
            elif function == 'prep-deluxe-po':
                # parse the invoices
                invoices = parse_deluxe_invoice(
                    self.upload_folder)
                # prep the PO
                prep_po(invoices, self.upload_folder)
                return redirect(url_for('download_files'))
            elif function == 'credits':
                get_credits(self.upload_folder)
                return redirect(url_for('download_files'))
            elif function == 'genre-trailer':
                write_genre_trailer(self.upload_folder)
                return redirect(url_for('download_files'))

        else:
            # the page title is the function without dashes and title cased
            return render_template('/upload/upload.html',
                                   file_type=file_type, function=function,
                                   title=function.replace('-', ' ').title())


class DownloadView(View):
    methods = ['GET', 'POST']

    def __init__(self):
        self.download_folder = current_app.config['DOWNLOAD_FOLDER']

    def dispatch_request(self):

        files = os.listdir(self.download_folder)
        base_path = pathlib.Path(self.download_folder)

        if request.method == 'POST':
            data = io.BytesIO()

            with zipfile.ZipFile(data, mode='w') as z:
                for item in base_path.iterdir():
                    z.write(item, os.path.basename(item))

            data.seek(0)

            return send_file(data, mimetype='application/zip',
                             as_attachment=True,
                             download_name='files.zip')
        else:
            return render_template('download/download.html',
                                   files=files, title='Download files')
