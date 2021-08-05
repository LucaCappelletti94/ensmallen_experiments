from ensmallen_experiments import retrieve_graphs
from tqdm.auto import tqdm
import shutil
import os


def test_graph_retrieval():
    """Test that the load graph benches work."""
    metadata_path = "tests/test_graphs.json"
    root = "tests/graphs"
    if os.path.exists(root):
        shutil.rmtree(root)
    retrieve_graphs(metadata_path, root)
    retrieve_graphs(metadata_path, root)