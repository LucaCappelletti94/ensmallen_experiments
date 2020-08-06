"""Methods to automatically retrieve, extract and clean the graph files."""
from .utils import extract, logger
import pandas as pd
import os
from tqdm.auto import tqdm
from encodeproject import download
from .sanitize_csv import sanitize_csv
from .normalize_csv import normalize_csv


def retrieve_graphs(
    path: str, 
    root: str = "graphs", 
    normalized_filename: str = "normalized_graph.tsv", 
    sanitized_filename: str = "sanitized_graph.tsv"
    ):
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
        folder = os.path.join(root, row.folder_name)

        path = os.path.join(root, row.url.split("/")[-1])
        if not os.path.exists(path):
            logger.info("Downloading %s -> %s", row.url, path)
            download(row.url, path, cache=True)

        extracted_folder = os.path.join(folder, row.extraction_path).strip("/")
        if not os.path.exists(extracted_folder):
            logger.info("Extracting %s -> %s", path, extracted_folder)
            extract(path, extracted_folder)

        extracted_file = os.path.join(folder, row.edge_file)
        normalized_file = os.path.join(folder, normalized_filename)
        if not os.path.exists(normalized_file):
            logger.info("Normalizing %s -> %s", extracted_file, normalized_file)
            normalize_csv(row, extracted_file, normalized_file)

        sanitized_file = os.path.join(folder, sanitized_filename)
        if not os.path.exists(sanitized_file):
            logger.info("Sanitizing %s -> %s", normalized_file, sanitized_file)
            sanitize_csv(normalized_file, sanitized_file, row)
