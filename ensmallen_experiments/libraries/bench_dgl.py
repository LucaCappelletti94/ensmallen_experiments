"""Submodule with methods from DGL to benchmark."""
from typing import Dict
import numpy as np
import dgl
from ..utils import build_directed_path


def load_graph_dgl(
    graph_name: str,
    repository: str,
    version: str,
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
    graph_name: str,
        Name of the graph to load.
    repository: str,
        Repository from where to load the graph.
    version: str,
        Version of the graph to load.
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    edge_path=build_directed_path(
        graph_name=graph_name,
        repository=repository,
        version=version,
        undirected=True
    )
    data = np.genfromtxt(edge_path, delimiter='\t')
    graph = dgl.graph((data[:, 0].astype(int), data[:, 1].astype(int)), )
    if has_weights:
        graph.edata['weights'] = data[:, 2]
    return graph


def execute_first_order_walk_dgl(
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
    return [
        dgl.sampling.random_walk(
            graph,
            nodes=np.arange(graph.num_nodes),
            length=length,
        )
        for i in iterations
    ]