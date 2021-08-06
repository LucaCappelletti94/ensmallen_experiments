from typing import Dict
import os
from ensmallen_graph import EnsmallenGraph
import compress_json


def build_directed_path(
    graph_name: str,
    repository: str,
    version: str,
    undirected: bool
) -> str:
    """Build path to edge file from given metadata."""
    return os.path.join(
        "graphs",
        repository,
        graph_name,
        version,
        "preprocessed",
        "undirected" if undirected else "directed",
        "edges.tsv"
    )


def build_graph_path(graph_name: str, root: str) -> str:
    """Build path to graph directory where to store the graph file and its results."""
    return os.path.join(
        root,
        graph_name
    )


def build_graph_report_path(graph_name: str, root: str) -> str:
    """Build path to edge file from given metadata."""
    return os.path.join(
        build_graph_path(graph_name, root),
        "report.json"
    )


def get_graph_report(graph_name: str, root: str) -> Dict:
    """Build path to edge file from given metadata."""
    return compress_json.load(build_graph_report_path(graph_name, root))["report"]


def store_graph_report(graph: EnsmallenGraph, graph_name: str, root: str) -> Dict:
    """Build path to edge file from given metadata."""
    return compress_json.dump(
        {
            "textual_report": graph.textual_report(),
            "report": graph.report()
        },
        build_graph_report_path(graph_name, root)
    )
