from typing import Dict
import os
import compress_json


def build_directed_path(root: str, directed: bool) -> str:
    """Build path to edge file from given metadata."""
    return os.path.join(root, "{}_sanitized.tsv".format("directed" if directed else "undirected"))


def build_path_path(data: Dict[str, str], root: str) -> str:
    """Build path to edge file from given metadata."""
    return os.path.join(root, data["folder_name"])


def get_graph_report(data: Dict, root: str) -> Dict:
    """Build path to edge file from given metadata."""
    return compress_json.load(os.path.join(build_path_path(data, root), "report.json"))
