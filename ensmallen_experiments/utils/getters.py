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


def get_walks_libraries_names() -> List[str]:
    """Return name of available libraries that execute walks."""
    return [
        library
        for library, data in libraries.items()
        if "execute_walks" in data
    ]


def get_graph_names(metadata_path: str) -> List[str]:
    """Return name of available graphs."""
    return list(compress_json.load(metadata_path).keys())
