"""Submodule with methods from Node2Vec to benchmark."""
from node2vec import Node2Vec
import networkx as nx
import numpy as np
from multiprocessing import cpu_count


def execute_walks_node2vec(
    graph: nx.Graph,
    length: int,
    iterations: int,
    p: float = 1.0,
    q: float = 1.0,
    **kwargs: Dict
) -> np.ndarray:
    """Execute first/second order walks using Ensmallen walker.

    Parameters
    --------------------------
    graph: nx.Graph,
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
    kwargs: Dict,
        Additional parameters to be used in other libraries but not this one.

    Returns
    --------------------------
    Computed walks as numpy array.
    """
    return Node2Vec(
        graph,
        quiet=True,
        walk_length=length,
        num_walks=iterations,
        workers=cpu_count(),
        p=p,
        q=q
    ).walks
