"""Module with methods to handle extraction of zip files."""
import gzip
import shutil


def ungzip(source: str, destination: str):
    """Extract given compress file from given source to given destination.

    Parameters
    ---------------------------
    source: str,
        The compress file.
    destination: str,
        The destination for the compress file.
    """
    with gzip.open(source, 'rb') as f_in:
        with open(destination, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
