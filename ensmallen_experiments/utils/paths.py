from typing import Dict
import os
from ensmallen_graph import EnsmallenGraph
import compress_json


def build_directed_path(root: str, directed: bool) -> str:
    """Build path to edge file from given metadata."""
    return os.path.join(root, "{}.tsv".format("directed" if directed else "undirected"))


def build_graph_path(data: Dict[str, str], root: str) -> str:
    """Build path to graph directory where to store the graph file and its results."""
    return os.path.join(
        root,
        data["graph_name"],
    )


def build_graph_report_path(data: Dict[str, str], root: str) -> str:
    """Build path to edge file from given metadata."""
    return os.path.join(
        build_graph_path(data, root),
        "report.json"
    )


def get_graph_report(data: Dict, root: str) -> Dict:
    """Build path to edge file from given metadata."""
    return compress_json.load(build_graph_report_path(data, root))


def store_graph_report(graph: EnsmallenGraph, data: Dict, root: str) -> Dict:
    """Build path to edge file from given metadata."""
    return compress_json.dump(
        {
            "textual_report": graph.textual_report(),
            "report": graph.report()
        },
        build_graph_report_path(data, root)
    )
