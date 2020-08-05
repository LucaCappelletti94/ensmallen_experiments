"""Module with methods to handle extraction of zip files."""
import zipfile
import shutil


def unzip(source: str, destination: str):
    """Extract given compress file from given source to given destination.

    Parameters
    ---------------------------
    source: str,
        The compress file.
    destination: str,
        The destination for the compress file.
    """
    with zipfile.ZipFile(source, 'r') as zip_ref:
        zip_ref.extractall(destination)
