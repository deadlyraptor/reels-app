import io
import os
import pathlib
import zipfile

from flask import (Blueprint, current_app, flash, redirect, request,
                   render_template, send_file, url_for)

from werkzeug.utils import secure_filename

from reels_app.po.utils import create_po, parse_deluxe_invoice

po = Blueprint('po', __name__)


@po.route('/upload-po-template', methods=['GET', 'POST'])
def upload_po_template():
    """Upload a PO template to the server."""

    if request.method == 'POST':

        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No file selected', 'warning')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['PO_FOLDER'],
                    secured_uploaded_file
                ))
        flash('PO template successfully uploaded', 'success')
        return redirect(url_for('po.upload_deluxe_invoices'))

    return render_template('upload/upload-po-template.html',
                           title='Purchase Order')


@po.route('/upload-deluxe-invoices', methods=['GET', 'POST'])
def upload_deluxe_invoices():
    """Upload Deluxe invoices for use with the PO."""

    if request.method == 'POST':

        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No file selected', 'warning')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['INVOICE_FOLDER'],
                    secured_uploaded_file
                ))
        flash('Deluxe invoices successfully uploaded', 'success')

        # parse the invoices
        invoices = parse_deluxe_invoice(
            current_app.config['INVOICE_FOLDER'])
        # create the PO
        create_po(invoices)
        return redirect(url_for('po.download_purchase_order'))

    return render_template('upload/upload-deluxe-invoices.html',
                           title='Upload Deluxe invoices')


@po.route('/download-purchase-order', methods=['GET', 'POST'])
def download_purchase_order():
    files = os.listdir(current_app.config['PO_FOLDER'])

    base_path = pathlib.Path(current_app.config['PO_FOLDER'])

    if request.method == 'POST':
        data = io.BytesIO()

        with zipfile.ZipFile(data, mode='w') as z:
            for item in base_path.iterdir():
                z.write(item, os.path.basename(item))

        data.seek(0)

        return send_file(data, mimetype='application/zip',
                         as_attachment=True,
                         download_name='po.zip')

    return render_template('download/download-files.html', files=files,
                           file_type='.xlsx', title='Download PO')
