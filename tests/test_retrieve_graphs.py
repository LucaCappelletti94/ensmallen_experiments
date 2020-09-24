"""Test suite to check that the retrieval and sanitization of the graphs works."""
import os
from ensmallen_experiments import retrieve_graphs


def test_retrieve_graphs():
    """Test that the retrieval of the graph works."""
    metadata_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "test_graphs.json"
    )
    retrieve_graphs(metadata_path, root="tests/graphs")
