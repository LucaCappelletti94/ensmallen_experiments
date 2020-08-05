import os
from ensmallen_experiments import retrieve_graphs

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

def test_pipeline():
    retrieve_graphs(os.path.join(TEST_DIR, "test_graphs.json"))
