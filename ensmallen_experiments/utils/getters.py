"""Module with getters utility methods."""
from typing import List
import compress_json
from ..libraries import libraries


def get_graph_libraries_names() -> List[str]:
    """Return name of available libraries that load graphs."""
    return [
        library
        for library, data in libraries.items()
        if "load_graph" in data
    ]


def get_first_order_walk_libraries_names() -> List[str]:
    """Return name of available libraries that execute walks."""
    return [
        library
        for library, data in libraries.items()
        if "first_order_walk" in data
    ]


def get_second_order_walk_libraries_names() -> List[str]:
    """Return name of available libraries that execute walks."""
    return [
        library
        for library, data in libraries.items()
        if "second_order_walk" in data
    ]


def get_graph_names(metadata_path: str) -> List[str]:
    """Return name of available graphs."""
    return [
        g["graph_name"]
        for g in compress_json.load(metadata_path)
        if not g["disabled"]
    ]


def get_graph_data_from_graph_name(metadata_path: str, graph_name: str) -> Dict:
    if graph_name not in get_graph_names(metadata_path):
        raise ValueError(
            (
                "Graph with name `{}` is not available."
            ).format(graph_name)
        )
    for graph_data in compress_json.load(metadata_path):
        if graph_data["graph_name"] == graph_name:
            return graph_data
