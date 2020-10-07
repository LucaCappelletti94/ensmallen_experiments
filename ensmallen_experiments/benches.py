from .libraries import libraries
from .utils import build_path_path, get_graph_report
import compress_json


def bench_load_graph(library: str, graph: str, metadata_path: str, root: str):
    """Benches loading the given graph using given library.

    Parameters
    -----------------------
    library: str,
        Library to use for the benchmark.
    graph: str,
        Graph to use for the benchmark.
    metadata_path: str,
        Path from where to load the graph metadata.
    root: str,
        Directory from where to load the graph.
    """
    if library not in libraries:
        raise ValueError(
            "Given library {} is not currently available for running benchmarks.".format(
                libraries
            )
        )
    metadata = compress_json.load(metadata_path)
    if graph not in metadata:
        raise ValueError(
            "Given graph {} is not currently available for running benchmarks.".format(
                libraries)
        )
    data = metadata[graph]
    report = get_graph_report(data, root)

    libraries[library]["load_graph"](
        edge_path=build_path_path(metadata[graph], root),
        nodes_number=int(report["nodes_number"]),
        edges_number=int(report["edges_number"]),
        has_weights=report["has_weights"]=="true"
    )
