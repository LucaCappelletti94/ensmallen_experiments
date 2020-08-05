import pandas as pd
from ensmallen_graph import EnsmallenGraph

def sanitize_csv(src_file: str, dst_file: str, row: pd.Series):
    kwargs = {
        "edge_path":src_file,
        "sources_column":"subject",
        "destinations_column":"object",
        "directed":False,
        "force_conversion_to_undirected":True,
        "ignore_duplicated_edges":True,
    }
    if not pd.isna(row.weight_col):
        kwargs["weights_column"] = "weight"
    EnsmallenGraph.from_csv(**kwargs).to_edges_csv(dst_file)