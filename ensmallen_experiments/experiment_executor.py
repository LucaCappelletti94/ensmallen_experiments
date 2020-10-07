import shlex
import subprocess
from time import sleep


def run_experiment(graph: str, library: str, task: str):
    p = subprocess.Popen(
        "python run_experiment.py",
        shell=True
    )
    print("DONER {}".format(p.pid))

    try:
        p.wait(timeout=30)
    except subprocess.TimeoutExpired:
        print("KILLED")
        p.kill()

    print("KEBAP")