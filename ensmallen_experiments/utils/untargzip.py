"""Module with methods to handle extraction of zip files."""
import tarfile
import shutil


def untargzip(source: str, destination: str):
    """Extract given compress file from given source to given destination.

    Parameters
    ---------------------------
    source: str,
        The compress file.
    destination: str,
        The destination for the compress file.
    """
    with tarfile.open(source, "r:gz") as tar:
        tar.extractall(destination)
