import pandas as pd
import os
from .utils import logger
from ensmallen_graph import EnsmallenGraph  # pylint: disable=no-name-in-module
from .utils import logger


def sanitize_csv(src_file: str, dst_file: str, row: pd.Series):
    try:
        kwargs = {
            "edge_path": src_file,
            "sources_column": "subject",
            "destinations_column": "object",
            "directed": False,
            "force_conversion_to_undirected": True,
            "ignore_duplicated_edges": True,
        }
        if not pd.isna(row.weight_col):
            kwargs["weights_column"] = "weight"
        EnsmallenGraph.from_csv(**kwargs).to_edges_csv(dst_file)

    except Exception as e:
        logger.error(
            "Error while sanitizing file at path {}.".format(src_file))
        if os.path.exists(dst_file):
            os.remove(dst_file)
        raise e
