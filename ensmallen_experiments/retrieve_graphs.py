"""Methods to automatically retrieve, extract and clean the graph files."""
from .utils import extract
import pandas as pd
import os
from tqdm.auto import tqdm
from encodeproject import download


def retrieve_graphs(path: str, root: str = "graphs"):
    """Retrieve graphs in given dataframe.

    Parameters
    ---------------------
    path: str,
        Path from where to load the graph informations.
    root: str = "graphs",
        Position where to download graphs
    """
    graphs = pd.read_json(path)
    for _, row in tqdm(
        graphs.iterrows(),
        desc="Downloading graphs",
        total=len(graphs)
    ):
        path = "{root}/{path}".format(
            root=root,
            path=row.url.split("/")[-1]
        )
        target = "{root}/{path}".format(
            root=root,
            path=row.extraction_path
        )
        download(row.url, path, cache=True)
        if os.path.exists(target):
            continue
        extract(path, target)
