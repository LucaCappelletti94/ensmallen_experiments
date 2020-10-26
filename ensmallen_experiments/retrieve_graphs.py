"""Methods to automatically retrieve, extract and clean the graph files."""
import compress_json
from .download_graphs import download_graphs
from .sanitize_graphs import sanitize_graphs
from .utils import extract, logger


def retrieve_graphs(
    informations_path: str,
    root: str = "graphs"
):
    """Retrieve graphs in given dataframe.

    Parameters
    ---------------------
    informations_path: str,
        Path from where to load the graph informations.
    root: str = "graphs",
        Position where to download graphs
    """
    # First we load the graphs metadata
    graphs_data = compress_json.load(informations_path)
    # First we proceed to download the graphs in multi-processing
    # If there is a failure while downloading the graph, the library automatically
    # cleans afer itself and afterwards raises the exception.
    download_graphs(graphs_data, root)
    raise ValueError("For now stopping here")
    # Secondly we sanitize the downloaded files to remove elements such as:
    # - file headers (descriptors added in top of the files that include licenses etc...)
    # - duplicated edges (in some file there are duplicated edges)
    sanitize_graphs(graphs_data, root)
