import os


def delete_files(directory):
    for item in os.listdir(directory):
        os.remove(os.path.join(directory, item))
