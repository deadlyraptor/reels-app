import os

from dotenv import load_dotenv
load_dotenv()


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    PHOTOS_FOLDER = 'uploads/photos'
    SPREADSHEET_FOLDER = 'uploads/spreadsheets'
