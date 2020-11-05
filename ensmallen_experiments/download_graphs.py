"""Methods to automatically download the graph files."""
import os
from multiprocessing import Pool, cpu_count
from typing import Dict
from glob import glob
import compress_json
import pandas as pd
from encodeproject import download
from tqdm.auto import tqdm

from .utils import extract, logger


def download_graph(graph_data: Dict, root: str):
    """Download and extract the given graph_data.

    Parameters
    ---------------------------
    graph_data: Dict,
        The dictionary with the metadata.
    root: str,
        The root of the directory where to store the files.
    """
    url = graph_data["url"]
    folder = os.path.join(root, graph_data["folder_name"])
    path = os.path.join(root, url.split("/")[-1])
    if not os.path.exists(path):
        try:
            logger.info("Downloading %s -> %s", url, path)
            download(url, path, cache=True)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            raise e

    extracted_folder = os.path.join(
        folder, graph_data.get("extraction_path", "")).strip("/")
    if not os.path.exists(extracted_folder):
        logger.info("Extracting %s -> %s", path, extracted_folder)
        extract(path, extracted_folder)


def _job(kwargs):
    """Wrapper for multi-processing."""
    download_graph(**kwargs)


def download_graphs(graphs_data: Dict, root: str):
    """download graphs in given dataframe.

    Parameters
    ---------------------
    graphs_data: Dict,
        Path from where to load the graph informations.
    root: str,
        Position where to download graphs
    """

    tasks = [
        dict(graph_data=graph_data, root=root)
        for graph_data in graphs_data.values()
    ]

    with Pool(min(cpu_count(), len(graphs_data))) as p:
        list(tqdm(
            p.imap(_job, tasks),
            desc="Retrieving graphs",
            total=len(graphs_data)
        ))
        p.close()
        p.join()
