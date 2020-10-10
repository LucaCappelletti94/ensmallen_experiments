import os
import pytest
from ensmallen_experiments.tracker import Tracker
from time import sleep

TEST_FILE = "test.log"

def test_load_graphs_benches():
    with Tracker(TEST_FILE):
        sleep(4)

    assert os.path.exists(TEST_FILE)

    with open(TEST_FILE) as f:
        txt = f.read()

    assert len(txt.split("\n")) > 1000