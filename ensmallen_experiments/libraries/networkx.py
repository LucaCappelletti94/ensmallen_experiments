"""Submodule with methods from Networkx to benchmark."""
from typing import Dict
import networkx as nx


def load_graph(
    edge_path: str,
    has_weights: bool,
    **kwargs: Dict
) -> nx.Graph:
    """Load graph object using Networkx.

    Parameters
    -----------------------
    edge_path: str,
        Path from where to load the edgelist.
        File is expected to be in directed fashion and sorted.
        The node IDs will be extracted from the numeric node IDs of the graph.
        The file is expected to be without header and the first column
        is expected to be the sources, while the second is expected to be
        the destinations. The third column, optionally, is expected to
        contain the weights if they are present in the considered graph.
    has_weights: bool,
        Wether the graph has weights and we should load them.
        The weights, if present, are expected to be in column 3.
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    if has_weights:
        return nx.read_weighted_edgelist(
            edge_path,
            delimiter="\t",
        )

    return nx.read_edgelist(
        edge_path,
        data=False,
        delimiter="\t",
    )
