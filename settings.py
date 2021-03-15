import os

from dotenv import load_dotenv
load_dotenv()


def validate_directory(directory):
    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)


validate_directory('csvs')
validate_directory('uploads')
validate_directory('uploads/spreadsheets')
validate_directory('uploads/photos')


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    PHOTOS_FOLDER = 'uploads/photos'
    SPREADSHEET_FOLDER = 'uploads/spreadsheets'
