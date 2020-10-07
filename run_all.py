#!~/anaconda3/bin/python
import os
import sys
import json
import shlex
import logging
import argparse
import subprocess
from tqdm.auto import tqdm
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)-15s[%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info":logging.INFO,
    "warn":logging.WARN,
    "warning":logging.WARNING,
    "error":logging.ERROR,
    "critical":logging.CRITICAL
}

def run_experiment(graph: str, library: str, task: str, executor_path: str, timeout_seconds:int = 3600):
    command = "python {executor_path}/run_experiment.py run {graph} {library} {task}".format(**locals())
    logger.info("Running {}".format(command))
    p = subprocess.Popen(
        shlex.split(command),
        shell=True
    )
    logger.info("Process spanwed with pid {}".format(p.pid))
    try:
        p.wait(timeout=timeout_seconds)
        logger.info("Process with pid {} terminated".format(p.pid))
    except subprocess.TimeoutExpired:
        logger.warn("Process with pid {} killed becasue it timedout".format(p.pid))
        p.kill()


def run_experiments(**kwargs):
    graphs = json.loads(subprocess.check_output("python {entrypoint} list graphs".format(**kwargs), shell=True))
    tasks  = json.loads(subprocess.check_output("python {entrypoint} list tasks".format(**kwargs), shell=True))
    for graph in tqdm(graphs):
        for task in tqdm(tasks):
            libraries = json.loads(subprocess.check_output("python {entrypoint} list libraries {task}".format(**kwargs), shell=True))
            for library in tqdm(libraries):
                run_experiment(graph=graph, task=task, library=library, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--entrypoint", type=str, help="Path to the entrypoint to execute", default="run_experiment.py")
    parser.add_argument("-m", "--metadata", type=str, help="Path to where to load the experiments metadata", default="./graphs.json")
    parser.add_argument("-r", "--root", type=str, help="Path to where to load the experiments metadata", default=os.path.abspath(os.path.dirname(__file__)))
    parser.add_argument("-v", "--verbosity", type=str, help="Lowercase log level. Default='error'", default="error")

    values= vars(parser.parse_args())
    values["metadata"] = os.path.join(values["root"], values["metadata"])
    values["entrypoint"] = os.path.join(values["root"], values["entrypoint"])

    if values["verbosity"].lower() not in LOG_LEVELS:
        logger.error("The verbosity level {} not known. The available ones are {}".format(values["verbosity"], list(LOG_LEVELS.keys())))
        sys.exit(1)

    logger.setLevel(LOG_LEVELS[values.pop("verbosity").lower()])

    run_experiments(**values)