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
    cache_size: float = None,
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

    if cache_size is not None:
        graph.enable_fast_walk(
            vector_destinations=False,
            vector_outbounds=False,
            cache_size=cache_size
        )

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


def load_graph_ensmallen_5_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 5% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.05, **kwargs)


def load_graph_ensmallen_10_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 10% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.1, **kwargs)


def load_graph_ensmallen_15_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 15% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.15, **kwargs)


def load_graph_ensmallen_20_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 20% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.20, **kwargs)


def load_graph_ensmallen_25_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 25% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.25, **kwargs)


def load_graph_ensmallen_30_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 30% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.30, **kwargs)


def load_graph_ensmallen_35_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 35% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.35, **kwargs)


def load_graph_ensmallen_40_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 40% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.40, **kwargs)


def load_graph_ensmallen_45_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 45% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.45, **kwargs)


def load_graph_ensmallen_50_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 50% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.50, **kwargs)


def load_graph_ensmallen_55_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 55% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.55, **kwargs)


def load_graph_ensmallen_60_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 60% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.60, **kwargs)


def load_graph_ensmallen_65_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 65% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.65, **kwargs)


def load_graph_ensmallen_70_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 70% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.70, **kwargs)


def load_graph_ensmallen_75_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 75% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.75, **kwargs)


def load_graph_ensmallen_80_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 80% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.80, **kwargs)


def load_graph_ensmallen_85_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 85% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.85, **kwargs)


def load_graph_ensmallen_90_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 90% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.90, **kwargs)


def load_graph_ensmallen_95_percent_cache(
    **kwargs: Dict
) -> EnsmallenGraph:
    """Load graph object using EnsmallenGraph with 95% cache.

    Parameters
    -----------------------
    **kwargs: Dict,
        Additional parameters that are used in other libraries but not this one.

    Returns
    -------------------------
    The loaded graph.
    """
    return load_graph_ensmallen(cache_size=0.95, **kwargs)


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
