import pytest
from ensmallen_experiments.utils import get_graph_libraries_names, get_first_order_walk_libraries_names, get_second_order_walk_libraries_names, get_graph_names
from ensmallen_experiments.benches import bench_load_graph, bench_first_order_walks, bench_second_order_walks
from ensmallen_experiments import retrieve_graphs
import compress_json
from tqdm.auto import tqdm
import shutil
import os


def test_load_graphs_benches():
    """Test that the load graph benches work."""
    metadata_path = "tests/test_graphs.json"
    root = "tests/graphs"
    if os.path.exists(root):
        shutil.rmtree(root)
    retrieve_graphs(metadata_path, root)
    for graph_data in tqdm(compress_json.load(metadata_path)):
        for library in tqdm(
            get_graph_libraries_names(),
            leave=False,
            desc="Testing available graph loading libraries"
        ):
            bench_load_graph(
                library=library,
                **graph_data,
                root=root
            )
        for library in tqdm(
            get_first_order_walk_libraries_names(),
            leave=False,
            desc="Testing available random walks libraries"
        ):
            bench_first_order_walks(
                library=library,
                **graph_data,
                root=root
            )
        # for library in tqdm(
        #     get_second_order_walk_libraries_names(),
        #     leave=False,
        #     desc="Testing available random walks libraries"
        # ):
        #     bench_second_order_walks(
        #         library,
        #         graph,
        #         metadata_path,
        #         root,
        #     )
