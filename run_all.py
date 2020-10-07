#!/usr/local/anaconda3/bin/python
import os
import json
import shlex
import logging
import argparse
import subprocess
from tqdm.auto import tqdm
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run_experiment(graph: str, library: str, task: str, executor_path: str, timeout_seconds:int = 3600):
    command = "{executor_path}/run_experiment.py {graph} {librar)y} {task}".format(**locals())
    logger.info("Running {}".format(command))
    p = subprocess.Popen(
        command,
        shell=True
    )
    logger.info("Process spanwed with pid {}".format(p.pid))
    try:
        p.wait(timeout=timeout_seconds)
        logger.info("Process with pid {} terminated".format(p.pid))
    except subprocess.TimeoutExpired:
        logger.info("Process with pid {} killed becasue it timedout".format(p.pid))
        p.kill()

def benchmark(**kwargs):
    print("Benchmarking graph: {graph} - task: {task} - library: {library}".format(**kwargs))


def run_experiments(**kwargs):
    graphs = json.loads(subprocess.check_output("{entrypoint} list graphs".format(**kwargs))
    tasks  = json.loads(subprocess.check_output("{entrypoint} list tasks".format(**kwargs)))
    for graph in tqdm(graphs):
        for task in tqdm(tasks):
            libraries = json.loads(subprocess.check_output("{entrypoint} list libraries {task}".format(**kwargs)))
            for library in tqdm(libraries):
                benchmark(graph=graph, task=task, library=library, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--entrypoint", type=str, help="Path to the entrypoint to execute", default="./run_experiment.py")
    parser.add_argument("-m", "--metadata", type=str, help="Path to where to load the experiments metadata", default="./graphs.json")
    parser.add_argument("-r", "--root", type=str, help="Path to where to load the experiments metadata", default=os.path.abspath(os.path.dirname(__file__)))

    values, arguments_left = parser.parse_known_args(sys.argv[1:])
    values["metadata_path"] = os.path.join(root, values["metadata_path"])
    values["entrypoint"] = os.path.join(root, values["entrypoint"])

    run_experiments(**values)