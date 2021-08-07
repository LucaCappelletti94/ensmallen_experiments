#!~/anaconda3/bin/python
import argparse
import gc
import json
import logging
import os
import shlex
import signal
import subprocess
import sys
from time import sleep, time

import psutil
from humanize import naturaldelta
from tqdm.auto import tqdm, trange

from ensmallen_experiments import retrieve_graphs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)-15s[%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

LIBRARY_TAKS_LIST = {
    "load": "graph_libraries",
    "first_order_walk": "first_order_walk",
    "second_order_walk": "second_order_walk",
    "second_order_walk_only_q": "second_order_walk_only_q",
    "second_order_walk_only_p": "second_order_walk_only_p",
}


def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        p.send_signal(sig)
    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)
    return (gone, alive)


def run_experiment(**kwargs):
    command = "python3 {executor_path} run {graph} {task} {library} {wait_time}".format(
        **kwargs)
    logger.info("Running {}".format(command))
    p = subprocess.Popen(
        command,
        shell=True
    )
    logger.info("Process spanwed with pid {}".format(p.pid))
    try:
        p.wait(timeout=kwargs["timeout"])
        logger.info("Process with pid {} terminated".format(p.pid))
    except subprocess.TimeoutExpired:
        logger.warning(
            "Process with pid {} killed because it timeouted".format(p.pid))
        kill_proc_tree(p.pid)


def run_experiments(**kwargs):
    graphs = kwargs.get("graphs", None) or json.loads(subprocess.check_output(
        "python3 {executor_path} list graphs".format(**kwargs), shell=True))
    tasks = kwargs.get("tasks", None) or json.loads(subprocess.check_output(
        "python3 {executor_path} list tasks".format(**kwargs), shell=True))
    retrieve_graphs(values["metadata"])
    for graph in tqdm(graphs, desc="Graphs"):
        for task in tqdm(tasks, desc="Tasks for {}".format(graph), leave=False):
            libraries = kwargs.get("libraries", None) or json.loads(subprocess.check_output(
                "python3 {executor_path} list {} ".format(LIBRARY_TAKS_LIST[task], **kwargs), shell=True))
            for library in tqdm(libraries, desc="Libraries for {}".format(task), leave=False):
                start = time()
                run_experiment(
                    graph=graph,
                    task=task,
                    library=library,
                    **kwargs
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--executor_path", type=str,
                        help="Path to the entrypoint to execute", default="run_experiment.py")
    parser.add_argument("-m", "--metadata", type=str,
                        help="Path to where to load the experiments metadata", default="./graphs.json")
    parser.add_argument("-r", "--root", type=str,
                        help="Path to where to load the experiments metadata", default="./graphs")
    parser.add_argument("-v", "--verbosity", type=str,
                        help="Lowercase log level. Default='error'", default="error")
    parser.add_argument("-g", "--graphs", type=str,
                        help="Optional, Which graphs to execute", action='append')
    parser.add_argument("-t", "--tasks", type=str,
                        help="Option, Which tasks to execute", action='append')
    parser.add_argument("-l", "--libraries", type=str,
                        help="Option, Which libraries to execute", action='append')
    parser.add_argument("-to", "--timeout", type=int,
                        help="After how many seconds to kill the experiment", default=60*60*4 + 10*60)
    parser.add_argument("-wt", "--wait-time", type=int,
                        help="How many seconds to wait after each experiment", default=2*60)

    values = vars(parser.parse_args())

    if values["verbosity"].lower() not in LOG_LEVELS:
        logger.error("The verbosity level {} not known. The available ones are {}".format(
            values["verbosity"], list(LOG_LEVELS.keys())))
        sys.exit(1)

    logger.setLevel(LOG_LEVELS[values.pop("verbosity").lower()])

    run_experiments(**values)
