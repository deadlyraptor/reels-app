import os

from dotenv import load_dotenv
load_dotenv()


def validate_directory(directory):
    """Check if directory exists, if not create it."""
    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)


# The directories to be created if they don't exist.
directories = ['csvs', 'pdfs', 'uploads', 'uploads/credits/',
               'uploads/spreadsheets', 'uploads/photos', 'uploads/pdfs',
               'uploads/invoices', 'uploads/purchase_order']

for directory in directories:
    validate_directory(directory)


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    CREDITS_FOLDER = 'uploads/credits'
    INVOICE_FOLDER = 'uploads/invoices'
    PHOTOS_FOLDER = 'uploads/photos'
    PDF_FOLDER = 'uploads/pdfs'
    PO_FOLDER = 'uploads/purchase_order'
    SPREADSHEET_FOLDER = 'uploads/spreadsheets'
