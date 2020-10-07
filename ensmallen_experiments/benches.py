from .libraries import libraries
from .utils import build_path_path, get_graph_report, get_graph_names
import compress_json


def validate_graph_and_library(library: str, graph: str, metadata_path: str):
    if library not in libraries:
        raise ValueError(
            "Given library {} is not currently available for running benchmarks.".format(
                libraries
            )
        )
    if graph not in get_graph_names(metadata_path):
        raise ValueError(
            "Given graph {} is not currently available for running benchmarks.".format(
                libraries
            )
        )


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
    validate_graph_and_library(library, graph, metadata_path)
    metadata = compress_json.load(metadata_path)
    data = metadata[graph]
    report = get_graph_report(data, root)

    libraries[library]["load_graph"](
        edge_path=build_path_path(metadata[graph], root),
        nodes_number=int(report["nodes_number"]),
        edges_number=int(report["edges_number"]),
        has_weights=report["has_weights"] == "true"
    )


def bench_random_walks(
    library: str,
    graph: str,
    metadata_path: str,
    root: str,
    length: int = 100,
    iterations: int = 1,
    p: float = 1.0,
    q: float = 1.0
):
    """Benches executing random walks the given graph using given library.

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
    p: float = 1.0,
        Inverse of the return weight.
    q: float = 1.0,
        Invert of the explore weight.
    """
    validate_graph_and_library(library, graph, metadata_path)
    metadata = compress_json.load(metadata_path)
    data = metadata[graph]
    report = get_graph_report(data, root)

    walkers = libraries[library]["execute_walks"]

    graph = walkers["load_graph"](
        edge_path=build_path_path(metadata[graph], root),
        nodes_number=int(report["nodes_number"]),
        edges_number=int(report["edges_number"]),
        has_weights=report["has_weights"] == "true"
    )

    walkers["walk"](
        graph,
        length=length,
        iterations=iterations,
        p=p,
        q=q
    )
