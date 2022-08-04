import os

from dotenv import load_dotenv
load_dotenv()


def validate_directory(directory):
    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)


validate_directory('csvs')
validate_directory('pdfs')
validate_directory('uploads')
validate_directory('uploads/spreadsheets')
validate_directory('uploads/photos')
validate_directory('uploads/pdfs')
validate_directory('uploads/invoices')
validate_directory('uploads/purchase_order')


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    PHOTOS_FOLDER = 'uploads/photos'
    SPREADSHEET_FOLDER = 'uploads/spreadsheets'
    PDF_FOLDER = 'uploads/pdfs'
    INVOICE_FOLDER = 'uploads/invoices'
    PO_FOLDER = 'uploads/purchase_order'
