"""Submodule with methods from Ensmallen to benchmark."""
from typing import Dict
from ensmallen_graph import EnsmallenGraph  # pylint: disable=no-name-in-module
import numpy as np
from ..utils import build_directed_path


def load_graph_ensmallen(
    edge_path: str,
    nodes_number: int,
    edges_number: int,
    has_weights: bool,
    fast: bool = False,
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph.

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
    nodes_number: int,
        Upper bound of nodes number present in the graph.
        The closer the number is to the actual number of nodes of the graph
        the better the compression performance are going to be.
    edges_number: int,
        Upper bound of edges number present in the graph.
        The closer the number is to the actual number of edges of the graph
        the better the compression performance are going to be.
    has_weights: bool,
        Wether the graph has weights and we should load them.
        The weights, if present, are expected to be in column 3.
    fast: bool = False,
        Wether to run the fast version that uses more memory.
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    graph: EnsmallenGraph = EnsmallenGraph.from_sorted_csv(
        build_directed_path(edge_path, directed=True),
        directed=False,
        nodes_number=nodes_number,
        edges_number=edges_number,
        sources_column_number=0,
        destinations_column_number=1,
        **(
            dict(weights_column_number=2)
            if has_weights else {}
        ),
        numeric_node_ids=True,
        verbose=False,
        edge_header=False
    )

    if fast:
        graph.enable_fast_walk()

    return graph


def load_graph_fast_ensmallen(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using fast EnsmallenGraph.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(fast=True, **kwargs)


def execute_walks_ensmallen(
    graph: EnsmallenGraph,
    length: int,
    iterations: int,
    p: float = 1.0,
    q: float = 1.0
) -> np.ndarray:
    """Execute first/second order walks using Ensmallen walker.

    Parameters
    --------------------------
    graph: EnsmallenGraph,
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
    return graph.complete_walks(
        length=length,
        iterations=iterations,
        return_weight=1/p,
        explore_weight=1/q
    )
