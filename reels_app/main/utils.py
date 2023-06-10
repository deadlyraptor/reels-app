import os


def delete_files(directory):
    """Delete all files in a directory."""
    for item in os.listdir(directory):
        os.remove(os.path.join(directory, item))
