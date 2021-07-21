"""Submodule with methods from DGL to benchmark."""
from typing import Dict, Union
import numpy as np
import dgl
from multiprocessing import cpu_count
from ..utils import build_directed_path


def load_graph_dgl(
    edge_path: str,
    has_weights: bool,
    **kwargs: Dict
) -> dgl.DGLGraph:
    """Load graph object using dgl.

    This method is based on the method provided by the jupyter notebook
    linked from the DGL library: https://github.com/dglai/WWW20-Hands-on-Tutorial/blob/master/basic_tasks/1_load_data.ipynb

    To be as fair as possible, we avoid using pandas which ay be slower and directly
    use numpy as the node IDs are all numeric and can be handled best with numpy directly.

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
    data = np.genfromtxt(edge_path, delimiter='\t')
    graph = dgl.graph((data[:, 0], data[:, 1]), )
    if has_weights:
        graph.edata['weights'] = data[:, 2]
    return graph


def execute_first_order_walk_igraph(
    graph: dgl.DGLGraph,
    length: int,
    iterations: int,
    **kwargs: Dict
) -> np.ndarray:
    """Execute first/second order walks using Ensmallen walker.

    Parameters
    --------------------------
    graph: dgl.DGLGraph,
        The graph on which to run the walks.
    length: int,
        Lenght of the walks.
    iterations: int,
        Number of walks to start from each node.
    kwargs: Dict,
        Additional parameters to be used in other libraries but not this one.

    Returns
    --------------------------
    Computed walks as numpy array.
    """
    return dgl.sampling.random_walk(
        graph,
        nodes=np.arange(graph.num_nodes),
        length=length,
    )
