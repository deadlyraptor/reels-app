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
directories = ['csvs', 'pdfs', 'downloads', 'uploads',
               'uploads/photos', 'uploads/spreadsheets']

for directory in directories:
    validate_directory(directory)


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = 'uploads/files'
    DOWNLOAD_FOLDER = 'downloads'
    PHOTOS_FOLDER = 'uploads/photos'
    SPREADSHEET_FOLDER = 'uploads/spreadsheets'
