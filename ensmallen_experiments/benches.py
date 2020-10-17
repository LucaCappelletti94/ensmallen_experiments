import os
import gc
from time import sleep
import compress_json

from .libraries import libraries
from .tracker import Tracker
from .utils import build_path_path, get_graph_names, get_graph_report


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


def wait_10_minutes():
    for _ in range(60*10):
        sleep(1)
        # Should not be necessary but apparently it is.
        gc.collect()


def bench_load_graph(library: str, graph_name: str, metadata_path: str, root: str):
    """Benches loading the given graph using given library.

    Parameters
    -----------------------
    library: str,
        Library to use for the benchmark.
    graph_name: str,
        Graph to use for the benchmark.
    metadata_path: str,
        Path from where to load the graph metadata.
    root: str,
        Directory from where to load the graph.
    """
    validate_graph_and_library(library, graph_name, metadata_path)
    metadata = compress_json.load(metadata_path)
    data = metadata[graph_name]
    report = get_graph_report(data, root)

    log_path = "{root}/results/{graph}/{library}/load_graph.csv".format(
        root=root,
        graph=graph_name,
        library=library
    )

    if os.path.exists(log_path):
        return

    with Tracker(log_path):
        libraries[library]["load_graph"](
            edge_path=build_path_path(data, root),
            nodes_number=int(report["nodes_number"]),
            edges_number=int(report["edges_number"]),
            has_weights=report["has_weights"] == "true"
        )
    wait_10_minutes()


def bench_first_order_walks(
    library: str,
    graph_name: str,
    metadata_path: str,
    root: str,
    length: int = 100,
    iterations: int = 1,
):
    """Benches executing random walks the given graph using given library.

    Parameters
    -----------------------
    library: str,
        Library to use for the benchmark.
    graph_name: str,
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
    validate_graph_and_library(library, graph_name, metadata_path)
    metadata = compress_json.load(metadata_path)
    data = metadata[graph_name]
    report = get_graph_report(data, root)

    walkers = libraries[library]["first_order_walk"]

    log_path = "{root}/results/{graph_name}/{library}/first_order_walk.csv".format(
        root=root,
        graph_name=graph_name,
        library=library
    )

    if os.path.exists(log_path):
        return

    graph = walkers["load_graph"](
        edge_path=build_path_path(data, root),
        nodes_number=int(report["nodes_number"]),
        edges_number=int(report["edges_number"]),
        has_weights=report["has_weights"] == "true"
    )

    with Tracker(log_path):
        walkers["walk"](
            graph,
            length=length,
            iterations=iterations
        )
    wait_10_minutes()

def bench_second_order_walks(
    library: str,
    graph_name: str,
    metadata_path: str,
    root: str,
    length: int = 100,
    iterations: int = 1,
    p: float = 2.0,
    q: float = 2.0
):
    """Benches executing random walks the given graph using given library.

    Parameters
    -----------------------
    library: str,
        Library to use for the benchmark.
    graph_name: str,
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
    validate_graph_and_library(library, graph_name, metadata_path)
    metadata = compress_json.load(metadata_path)
    data = metadata[graph_name]
    report = get_graph_report(data, root)

    walkers = libraries[library]["second_order_walk"]

    log_path = "{root}/results/{graph_name}/{library}/second_order_walk.csv".format(
        root=root,
        graph_name=graph_name,
        library=library
    )

    if os.path.exists(log_path):
        return

    graph = walkers["load_graph"](
        edge_path=build_path_path(data, root),
        nodes_number=int(report["nodes_number"]),
        edges_number=int(report["edges_number"]),
        has_weights=report["has_weights"] == "true"
    )

    with Tracker(log_path):
        walkers["walk"](
            graph,
            length=length,
            iterations=iterations,
            p=p,
            q=q,
        )
    wait_10_minutes()