import pytest
from ensmallen_experiments.utils import get_graph_libraries_names, get_walks_libraries_names, get_graph_names
from ensmallen_experiments.benches import bench_load_graph, bench_random_walks
from ensmallen_experiments import retrieve_graphs
from tqdm.auto import tqdm
import shutil


def test_load_graphs_benches():
    """Test that the load graph benches work."""
    metadata_path = "tests/test_graphs.json"
    root = "tests/graphs"
    retrieve_graphs(metadata_path, root)
    for graph in tqdm(get_graph_names(metadata_path), desc="Testing available graphs"):
        for library in tqdm(get_graph_libraries_names(), desc="Testing available graph loading libraries"):
            bench_load_graph(
                library,
                graph,
                metadata_path,
                root
            )
        for library in tqdm(get_walks_libraries_names(), desc="Testing available random walks libraries"):
            bench_random_walks(
                library,
                graph,
                metadata_path,
                root
            )

    with pytest.raises(ValueError):
        bench_load_graph(
            "unexistant",
            get_graph_names(metadata_path)[0],
            metadata_path,
            root
        )

    with pytest.raises(ValueError):
        bench_load_graph(
            get_graph_libraries_names()[0],
            "unexistant",
            metadata_path,
            root
        )
    shutil.rmtree(root)
