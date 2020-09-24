import multiprocessing as mp
import os
from typing import Dict, List

import compress_json
from ensmallen_graph import EnsmallenGraph  # pylint: disable=no-name-in-module
from tqdm import tqdm

from .utils import logger


def sanitize_graph(graph_data: str, root: str):
    """Convert all the graphs to a standard format.
    
    Parameters
    ----------
    graph_data: List[Dict],
        Informations of the graph to sanitize
    root: str,
        The working folder. All the files will be read and written from here.
    """
    kwargs = graph_data["loading_settings"]

    kwargs["edge_path"] = os.path.join(
        root,
        graph_data["folder_name"],
        graph_data["edge_file"]
    )

    kwargs.setdefault("directed", True)

    logger.info("Loading the file %s"%kwargs["edge_path"])
    graph: EnsmallenGraph = EnsmallenGraph.from_csv(**kwargs)
    dst_path = os.path.join(
            root,
            graph_data["folder_name"],
            "sanitized.tsv"
        )
    logger.info("Writing the file %s"%dst_path)
    graph.dump_edges(
        path=dst_path,
        sources_column_number=0,
        destinations_column_number=1,
        weights_column_number=2,
    )

def sanitize_graphs(graphs_data: List[Dict], root: str):
    """Load all the graphs and convert them to a standard format.
    
    Parameters
    ----------
    graphs_data: List[Dict],
        The list of informations of all the graphs to sanitize
    root: str,
        The working folder. All the files will be read and written from here.
    """
    for graph_data in tqdm(
        graphs_data,
        desc="Retrieving graphs",
        total=len(graphs_data)
    ):
        sanitize_graph(graph_data, root)
