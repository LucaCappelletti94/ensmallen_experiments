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
    ]