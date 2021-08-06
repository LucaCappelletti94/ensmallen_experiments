from typing import Dict, List
import os
import gc
from time import sleep
import pandas as pd
import numpy as np
import compress_json

from .libraries import libraries
from .tracker import Tracker
from .utils import build_graph_path, get_graph_names, get_graph_report


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


def wait_k_seconds(k: int):
    """Sleeps for given amount of seconds running the garbage collector each time.

    Parameters
    -----------------------
    k: int,
        Number of seconds to sleep for.
    """
    for _ in range(k):
        sleep(1)
        # Should not be necessary but apparently it is.
        gc.collect()


def can_load(root: str, library: str, graph_name: str) -> bool:
    """Return boolean representing if given library can load the given graph."""
    path = "results/{graph}/{library}/load_graph.csv".format(
        root=root,
        graph=graph_name,
        library=library
    )
    if not os.path.exists(path):
        return False

    fp = open(path, "rb")
    if os.path.getsize(path) > 80:
        fp.seek(-80, 2)  # 2 means "from the end of the file"
    last_line = fp.readlines()[-1].decode("utf-8")
    fp.close()

    return set(last_line.strip()) == {"0", ","}


def load_graph(
    library: str,
    graph_name: str,
    repository: str,
    version: str,
    report: Dict,
    p: float = 1.0,
    q: float = 1.0
):
    """
    Parameters
    ---------------------------
    graph_name: str,
        Name of the graph to load.
    repository: str,
        Repository from where to load the graph.
    version: str,
        Version of the graph to load.
    """
    return libraries[library]["load_graph"](
        graph_name = graph_name,
        repository=repository,
        version=version,
        nodes_number=int(report["nodes_number"]),
        edges_number=int(report["directed_edges_number"]),
        density=float(report["density"]),
        has_weights=report["has_edge_weights"] == "true",
        p=p,
        q=q
    )


def bench_load_graph(
    library: str,
    graph_name: str,
    repository: str,
    version: str,
    root: str,
    seconds: int = 1
):
    """Benches loading the given graph using given library.

    Parameters
    -----------------------
    library: str,
        Library to use for the benchmark.
    graph_name: str,
        Name of the graph to load.
    repository: str,
        Repository from where to load the graph.
    version: str,
        Version of the graph to
    root: str,
        Directory from where to load the graph.
    seconds: int = 1,
        Number of seconds to wait for after a successfull execution.
    """
    report = get_graph_report(graph_name, root)

    log_path = "results/{graph}/{library}/load_graph.csv".format(
        root=root,
        graph=graph_name,
        library=library
    )

    if os.path.exists(log_path):
        return

    with Tracker(log_path):
        load_graph(
            library=library,
            graph_name=graph_name,
            repository=repository,
            version=version,
            report=report
        )

    wait_k_seconds(seconds)


def bench_first_order_walks(
    library: str,
    graph_name: str,
    metadata_path: str,
    root: str,
    seconds: int,
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
    seconds: int,
        Number of seconds to wait for after a successfull execution.
    length: int = 100,
        Length of the random walks.
    iterations: int = 1,
        Number of iterations to execute.
    """
    validate_graph_and_library(library, graph_name, metadata_path)
    metadata = compress_json.load(metadata_path)
    if "disabled" in metadata:
        return
    data = metadata[graph_name]
    report = get_graph_report(data, root)

    walkers = libraries[library]["first_order_walk"]

    log_path = "results/{graph_name}/{library}/first_order_walk.csv".format(
        root=root,
        graph_name=graph_name,
        library=library
    )

    # If the library has already been tracked we skip it.
    # The same applies also when it is known that the graph cannot be handled with this library.
    if os.path.exists(log_path) or not can_load(root, walkers["load_graph"], graph_name):
        return

    graph = load_graph(walkers["load_graph"], data, root, report)

    with Tracker(log_path):
        walkers["walk"](
            graph,
            length=length,
            iterations=iterations
        )
    wait_k_seconds(seconds)


def bench_second_order_walks(
    library: str,
    graph_name: str,
    metadata_path: str,
    root: str,
    seconds: int,
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
    seconds: int,
        Number of seconds to wait for after a successfull execution.
    length: int = 100,
        Length of the random walks.
    iterations: int = 1,
        Number of iterations to execute.
    p: float = 1.0,
        Inverse of the return weight.
    q: float = 1.0,
        Invert of the explore weight.
    """
    validate_graph_and_library(library, graph_name, metadata_path)
    metadata = compress_json.load(metadata_path)
    if "disabled" in metadata:
        return
    data = metadata[graph_name]
    report = get_graph_report(data, root)

    walkers = libraries[library]["second_order_walk"]

    if p == 2.0 and q == 1.0:
        task_name = "second_order_walk_only_p"
    elif q == 2.0 and p == 1.0:
        task_name = "second_order_walk_only_q"
    else:
        task_name = "second_order_walk"

    log_path = "results/{graph_name}/{library}/{task_name}.csv".format(
        root=root,
        graph_name=graph_name,
        library=library,
        task_name=task_name
    )

    # If the library has already been tracked we skip it.
    # The same applies also when it is known that the graph cannot be handled with this library.
    if os.path.exists(log_path) or not can_load(root, walkers["load_graph"], graph_name):
        return

    graph = load_graph(walkers["load_graph"], data, root, report, p=p, q=q)

    with Tracker(log_path):
        walkers["walk"](
            graph,
            length=length,
            iterations=iterations,
            max_degree=int(report["max_degree"]),
            nodes_number=int(report["nodes_number"]),
            p=p,
            q=q,
        )
    wait_k_seconds(seconds)
