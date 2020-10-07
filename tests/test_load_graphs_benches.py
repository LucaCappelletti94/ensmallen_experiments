import pytest
from ensmallen_experiments.utils import get_graph_libraries_names, get_graph_names
from ensmallen_experiments.benches import bench_load_graph
from tqdm.auto import tqdm


def test_load_graphs_benches():
    """Test that the load graph benches work."""
    metadata_path = "tests/test_graphs.json"
    root = "tests/graphs"
    for library in tqdm(get_graph_libraries_names(), desc="Testing available libraries"):
        for graph in tqdm(get_graph_names(metadata_path), desc="Testing available graphs"):
            bench_load_graph(
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
