"""Submodule with methods from pecampy to benchmark."""
from typing import Dict, Union
from pecanpy import node2vec
import numpy as np
from multiprocessing import cpu_count
from ..utils import build_directed_path


def load_graph_pecampy(
    edge_path: str,
    has_weights: bool,
    nodes_number: int,
    density: float,
    p: float,
    q: float,
    **kwargs: Dict
) -> Union[node2vec.PreComp, node2vec.SparseOTF, node2vec.DenseOTF]:
    """Load graph object using pecampy.

    Parameters
    -----------------------
    nodes_number: int,
        Number of nodes of the graph.
    edge_path: str,
        Path from where to load the edgelist.
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    edge_path = build_directed_path(edge_path, True)
    if nodes_number < 10000:
        graph = node2vec.PreComp(p, q, cpu_count(), verbose=False)
        graph.read_edg(edge_path, has_weights, False)
    elif density < 0.1:
        graph = node2vec.SparseOTF(p, q, cpu_count(), verbose=False)
        graph.read_edg(edge_path, has_weights, False)
    else:
        graph = node2vec.DenseOTF(p, q, cpu_count(), verbose=False)
        graph.read_edg(edge_path, has_weights, False)
    return graph


def execute_walks_pecampy(
    graph: Union[node2vec.PreComp, node2vec.SparseOTF, node2vec.DenseOTF],
    length: int,
    iterations: int,
    **kwargs
) -> np.ndarray:
    """Execute first/second order walks using pecampy walker.

    Parameters
    --------------------------
    graph: Union[node2vec.PreComp, node2vec.SparseOTF, node2vec.DenseOTF],
        The graph on which to run the walks.
    length: int,
        Lenght of the walks.
    iterations: int,
        Number of walks to start from each node.
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    --------------------------
    Computed walks as numpy array.
    """
    return graph.simulate_walks(iterations, length)
