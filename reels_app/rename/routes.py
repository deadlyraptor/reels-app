import os

from flask import (Blueprint, current_app, flash, redirect,
                   request, render_template, url_for)
from werkzeug.utils import secure_filename

rename = Blueprint('rename', __name__)


@rename.route('/rename', methods=['GET', 'POST'])
def upload_photos():
    if request.method == 'POST':

        uploaded_file = request.files['file']

        for uploaded_file in request.files.getlist('file'):
            if uploaded_file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            else:
                secured_uploaded_file = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(
                    current_app.config['PHOTOS_FOLDER'], secured_uploaded_file))
            flash('File successfully uploaded')
            return redirect(url_for('rename.upload_photos'))

    return render_template('rename.html', title='Rename Photos')


"""
import sys
import os

# tkinter is only used for directory prompt
root = tk.Tk()
root.withdraw()  # hides default window
directory = filedialog.askdirectory()

# if user does not select a directory, exit the script
if not directory:
    sys.exit()

base_name = input('Enter the new base filename: ')

# renames each photo in the selected directory
with os.scandir(directory) as photo_directory:
    for number, photo in enumerate(photo_directory, start=1):
        if photo.name.endswith(('.jpg', '.jpeg', '.png')):
            new_name = f'{base_name}-still-{str(number).zfill(2)}.{photo.name.split(".")[1]}'
            os.rename(photo, os.path.join(directory, new_name))
"""
