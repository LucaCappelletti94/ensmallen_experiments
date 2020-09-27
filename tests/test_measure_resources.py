"""Test suite to check that the retrieval and sanitization of the graphs works."""
import os
from time import sleep
from ensmallen_experiments import MeasureResources

def test_retrieve_graphs():
    """Test that the retrieval of the graph works."""
    tracker = MeasureResources()
    with tracker(name="test"):
        sleep(0.5)
        a = list(range(int(1e6)))
        sleep(0.5)
        del a
        sleep(0.5)
        
    with tracker(name="test2"):
        sleep(0.5)
        a = list(range(int(1e6)))
        sleep(0.5)
        del a
        sleep(0.5)

    with tracker(name="test3"):
        sleep(0.5)
        a = list(range(int(1e6)))
        sleep(0.5)
        del a
        sleep(0.5)

    tracker.get_results()