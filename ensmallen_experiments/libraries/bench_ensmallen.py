"""Submodule with methods from Ensmallen to benchmark."""
from typing import Dict
from ensmallen_graph import EnsmallenGraph  # pylint: disable=no-name-in-module
import numpy as np
from ..utils import build_directed_path


def load_graph_ensmallen(
    graph_name: str,
    repository: str,
    version: str,
    nodes_number: int,
    edges_number: int,
    has_weights: bool,
    fast: bool = False,
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph.

    Parameters
    -----------------------
    graph_name: str,
        Name of the graph to load.
    repository: str,
        Repository from where to load the graph.
    version: str,
        Version of the graph to
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
    graph: EnsmallenGraph = EnsmallenGraph.from_csv(
        build_directed_path(
            graph_name=graph_name,
            repository=repository,
            version=version,
            undirected=True
        ),
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
        edge_list_numeric_node_ids=True,
        verbose=False,
        edge_header=False,
        edge_list_is_complete=True,
        edge_list_may_contain_duplicates=False,
        edge_list_is_sorted=True,
        edge_list_is_correct=True,
        load_edge_list_in_parallel=True
    )

    if fast:
        graph.enable()

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
    nodes_number: int,
    max_degree: int,
    p: float = 1.0,
    q: float = 1.0,
    **kwargs: Dict
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
    nodes_number: int,
        Number of nodes in the graph.
    max_degree: int,
        Maximum degree of the graph.
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
    return graph.complete_walks(
        length=length,
        iterations=iterations,
        return_weight=1/p,
        explore_weight=1/q,
        max_neighbours=10_100 if max_degree > 10_000 and nodes_number > 500_000 else None
    )
