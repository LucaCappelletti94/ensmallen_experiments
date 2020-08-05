"""Module with methods to handle extraction of zip files."""
import os
from .ungzip import ungzip
from .unzip import unzip
from .untargzip import untargzip

methods = {
    "tar.gz": untargzip,
    "gz": ungzip,
    "zip": unzip
}


def extract(source: str, destination: str):
    """Extract given compress file from given source to given destination.

    This method automatically chooses the extraction method depending on the
    extension of the given source file.

    Parameters
    ---------------------------
    source: str,
        The compress file.
    destination: str,
        The destination for the compress file.

    Raises
    ---------------------------
    ValueError,
        If given source file has a destination that is not currently supported.
    """
    global methods
    # Create the directory if required.
    for path in (source, destination):
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    sorted_methods = sorted(
        methods.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    for ext, method in sorted_methods:
        # Extract the given file.
        if source.endswith(ext):
            method(source, destination)
            return

    raise ValueError(
        (
            "Given source file '{source}' has an extension which "
            "is not currently supported."
        ).format(source=source)
    )
