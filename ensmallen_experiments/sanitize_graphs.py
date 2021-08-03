import multiprocessing as mp
import os
from typing import Dict, List

import compress_json
from ensmallen_graph import EnsmallenGraph  # pylint: disable=no-name-in-module
from tqdm import tqdm

from .utils import logger


def sanitize_graph(graph_data: str, root: str):
    """Convert all the graphs to a standard format.

    Parameters
    ----------
    graph_data: List[Dict],
        Informations of the graph to sanitize
    root: str,
        The working folder. All the files will be read and written from here.
    """
    kwargs = graph_data["loading_settings"]

    kwargs["edge_path"] = os.path.join(
        root,
        graph_data["folder_name"],
        graph_data["edge_file"]
    )

    kwargs.setdefault("directed", False)

    directed_dst_path = os.path.join(
        root,
        graph_data["folder_name"],
        "directed_sanitized.tsv"
    )

    undirected_dst_path = os.path.join(
        root,
        graph_data["folder_name"],
        "undirected_sanitized.tsv"
    )

    report_path = os.path.join(
        root,
        graph_data["folder_name"],
        "report.json"
    )

    textual_report_path = os.path.join(
        root,
        graph_data["folder_name"],
        "report.txt"
    )

    if all(
        os.path.exists(p)
        for p in (directed_dst_path, undirected_dst_path, report_path, textual_report_path)
    ):
        return

    logger.info("Loading the file %s" % kwargs["edge_path"])
    graph: EnsmallenGraph = EnsmallenGraph.from_csv(
        **kwargs,
        name=graph_data["graph"]
    )
    logger.info("Enabling fast version")
    graph.enable()
    logger.info("Computing metadata")
    if not os.path.exists(report_path):
        logger.info("Computing JSON report")
        report = graph.report()
        compress_json.dump(report, report_path)
    if not os.path.exists(textual_report_path):
        logger.info("Computing textual report")
        textual_report = str(graph)
        with open(textual_report_path, "w") as f:
            f.write(textual_report)

    if not os.path.exists(undirected_dst_path):
        logger.info("Writing the file {}".format(undirected_dst_path))
        graph.dump_edges(
            path=undirected_dst_path,
            header=False,
            sources_column_number=0,
            destinations_column_number=1,
            weights_column_number=2,
            numeric_node_ids=True,
            # We dump with directed=True for the undirected file to have in the file the bidirectional edges.
            directed=True
        )
    if not os.path.exists(directed_dst_path):
        logger.info("Writing the file {}".format(directed_dst_path))
        graph.dump_edges(
            path=directed_dst_path,
            header=False,
            sources_column_number=0,
            destinations_column_number=1,
            weights_column_number=2,
            numeric_node_ids=True,
            # We dump with directed=False for the directed file to have no doubled bidirectional edge in the write out.
            directed=False
        )


def sanitize_graphs(graphs_data: List[Dict], root: str):
    """Load all the graphs and convert them to a standard format.

    Parameters
    ----------
    graphs_data: List[Dict],
        The list of informations of all the graphs to sanitize
    root: str,
        The working folder. All the files will be read and written from here.
    """
    for graph_data in tqdm(
        graphs_data.values(),
        desc="Retrieving graphs",
        total=len(graphs_data)
    ):
        if "disabled" in graph_data:
            continue
        sanitize_graph(graph_data, root)
