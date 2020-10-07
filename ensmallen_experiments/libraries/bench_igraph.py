"""Submodule with methods from iGraph to benchmark."""
from typing import Dict
from igraph import Graph
from ..utils import build_directed_path


def load_graph_igraph(
    edge_path: str,
    **kwargs: Dict
) -> Graph:
    """Load graph object using iGraph.

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
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return Graph.Read_Ncol(build_directed_path(edge_path, directed=True),  directed=False)
