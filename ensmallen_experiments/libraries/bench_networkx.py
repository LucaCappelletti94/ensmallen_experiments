"""Submodule with methods from Networkx to benchmark."""
from typing import Dict
import networkx as nx
from ..utils import build_directed_path


def load_graph_networkx(
    graph_name: str,
    repository: str,
    version: str,
    has_weights: bool,
    **kwargs: Dict
) -> nx.Graph:
    """Load graph object using Networkx.

    Parameters
    -----------------------
    graph_name: str,
        Name of the graph to load.
    repository: str,
        Repository from where to load the graph.
    version: str,
        Version of the graph to load.
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
            build_directed_path(
                graph_name=graph_name,
                repository=repository,
                version=version,
                undirected=True
            ),
            delimiter="\t",
        )

    return nx.read_edgelist(
        build_directed_path(
            graph_name=graph_name,
            repository=repository,
            version=version,
            undirected=True
        ),
        data=False,
        delimiter="\t",
    )
