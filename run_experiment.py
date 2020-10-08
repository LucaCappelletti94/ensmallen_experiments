#!/usr/local/anaconda3/bin/python
import os
import sys
import argparse
from ensmallen_experiments.utils import get_graph_libraries_names, get_walks_libraries_names, get_graph_names
from ensmallen_experiments.benches import bench_load_graph, bench_random_walks

def run_entrypoint(root, metadata_path, args):
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=str, help="Which graph to use for the experiment")
    parser.add_argument("task", type=str, help="Which task to benchmark for the experiment")
    parser.add_argument("library", type=str, help="Which library to use for the experiment")
    values = vars(parser.parse_args(args))
    graph, library, task = values["graph"], values["library"], values["task"]

    graphs = get_graph_names(metadata_path)
    if graph not in graphs:
        print("Graph [{}] not known. The available ones are {}".format(task, graphs))
        sys.exit(1)

    if task not in TASKS:
        print("Task [{}] not known. The available ones are {}".format(task, list(TASKS.keys())))
        sys.exit(1)

    if task == "load":
        libraries = get_graph_libraries_names()
    else:
        libraries = get_walks_libraries_names()

    if library not in libraries:
        print("Library [{}] not known. The available ones are {}".format(library, libraries))
        sys.exit(1)

    TASKS[task](
        library,
        graph,
        metadata_path,
        root
    )


def list_entrypoint(root, metadata_path, args):
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", type=str, help="What you want to list (graphs, libraries, tasks)")
    topic = vars(parser.parse_args(args))["topic"]
    
    if topic not in LISTS:
        print("The topic {} is not known. The available ones are {}".format(topic, list(LISTS.keys())))
        sys.exit(1)

    print(LISTS[topic](metadata_path))
    sys.exit(0)

TASKS = {
    "load":bench_load_graph,
    "first_order_walk":bench_random_walks,
    "second_order_walk":lambda *x: bench_random_walks(*x, p=2.0, q=2.0)
}
LISTS = {
    "graphs":get_graph_names,
    "graph_libraries":lambda _: get_graph_libraries_names,
    "walks_libraries":lambda _: get_walks_libraries_names,
    "tasks":list(TASKS.keys())
}
SUB_COMMANDS = {
    "run":run_entrypoint,
    "list":list_entrypoint,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main entrypoint for benchmarking")
    parser.add_argument("subcommand", type=str, help="Which subcommand to execute")
    parser.add_argument("-m", "--metadata", type=str, help="Path to where to load the experiments metadata", default="./graphs.json")
    parser.add_argument("-r", "--root", type=str, help="Path to where to load the experiments metadata", default="./graphs")

    values, arguments_left = parser.parse_known_args(sys.argv[1:])
    subcommand, metadata_path, root = values.subcommand, values.metadata, values.root

    if subcommand not in SUB_COMMANDS:
        print("Subcommand {} not known. The available ones are : {}".format(subcommand, list(SUB_COMMANDS.keys())))
        sys.exit(1)

    if not os.path.exists(metadata_path):
        print("The metadata file {} does not exists.".format(metadata_path))
        sys.exit(1)

    SUB_COMMANDS[subcommand](root, metadata_path, arguments_left)