"""Submodule with methods from CSRgraph to benchmark."""
from typing import Dict
import csrgraph as cg
import numpy as np
from ..utils import build_directed_path


def load_graph_csrgraph(
    edge_path: str,
    has_weights: bool,
    **kwargs: Dict
) -> cg.csrgraph:
    """Load graph object using CSRgraph.

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
    return cg.read_edgelist(
        build_directed_path(edge_path, directed=False),
        sep="\t",
    )


def execute_walks_csrgraph(
    graph: cg.csrgraph,
    length: int,
    iterations: int,
    p: float = 1.0,
    q: float = 1.0
) -> np.ndarray:
    """Execute first/second order walks using CSRgraph walker.

    Parameters
    --------------------------
    graph: CSRgraph,
        The graph on which to run the walks.
    length: int,
        Lenght of the walks.
    iterations: int,
        Number of walks to start from each node.
    p: float = 1.0,
        Inverse weight for making the walk local.
        By default, the walk will be uniform.
    q: float = 1.0,
        Inverse weight for making the walk a deep first.
        By default, the walk will be uniform.

    Returns
    --------------------------
    Computed walks as numpy array.
    """
    return graph.random_walks(
        walklen=length,
        epochs=iterations,
        return_weight=1/p,
        neighbor_weight=1/q
    )
