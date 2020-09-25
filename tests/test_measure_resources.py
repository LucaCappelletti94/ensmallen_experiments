"""Test suite to check that the retrieval and sanitization of the graphs works."""
import os
from time import sleep
from ensmallen_experiments import MeasureResources

TEST_FILE = "test_file.csv"

def test_retrieve_graphs():
    """Test that the retrieval of the graph works."""
    with MeasureResources(TEST_FILE):
        sleep(0.5)
        a = list(range(int(1e6)))
        sleep(0.5)
        del a
        sleep(0.5)

    assert os.path.exists(TEST_FILE)

    os.remove(TEST_FILE)