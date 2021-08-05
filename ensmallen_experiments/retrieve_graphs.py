"""Methods to automatically retrieve, extract and clean the graph files."""
import compress_json
from ensmallen_graph import EnsmallenGraph
from ensmallen_graph.datasets import get_dataset
from .utils import store_graph_report, logger


def retrieve_graphs(
    informations_path: str,
    root: str = "graphs"
):
    """Retrieve graphs in given dataframe.

    Parameters
    ---------------------
    informations_path: str,
        Path from where to load the graph informations.
    root: str = "graphs",
        Position where to download graphs
    """
    for graph_data in compress_json.load(informations_path):
        logger.info("Retrieving graph {}".format(graph_data["graph_data"]))
        for directed in (True, False):
            graph_generator = get_dataset(**graph_data)
            if graph_generator.is_preprocessed():
                continue
            graph: EnsmallenGraph = graph_generator(
                # We want to avoid loading edge types and node types
                # because we do not care for them in these benchmarks
                edge_list_edge_types_column_number=None,
                edge_list_edge_types_column=None,
                node_list_node_types_column_number=None,
                node_list_node_types_column=None,
                directed=directed
            )
        # We only store the report for the undirected version.
        store_graph_report(graph, graph_data, root)