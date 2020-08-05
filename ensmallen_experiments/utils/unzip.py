"""Module with methods to handle extraction of zip files."""
import subprocess


def unzip(source: str, destination: str):
    """Extract given compress file from given source to given destination.

    Parameters
    ---------------------------
    source: str,
        The compress file.
    destination: str,
        The destination for the compress file.
    """
    command = "unzip -q {source} -d {destination}".format(
        source=source,
        destination=destination
    )
    subprocess.call(command, shell=True)
