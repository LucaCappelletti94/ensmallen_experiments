#!/usr/local/anaconda3/bin/python
import os
import sys
import json
import argparse
from ensmallen_experiments.utils import get_graph_libraries_names, get_first_order_walk_libraries_names, get_second_order_walk_libraries_names, get_graph_names, get_graph_data_from_graph_name
from ensmallen_experiments.benches import bench_load_graph, bench_first_order_walks, bench_second_order_walks


def run_entrypoint(root, metadata_path, args):
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=str,
                        help="Which graph to use for the experiment")
    parser.add_argument(
        "task", type=str, help="Which task to benchmark for the experiment")
    parser.add_argument("library", type=str,
                        help="Which library to use for the experiment")
    parser.add_argument("seconds", type=int,
                        help="How many seconds to wait after each experiment", default=2*60)
    values = vars(parser.parse_args(args))
    graph_name, library, task, seconds = values["graph"], values["library"], values["task"], values["seconds"]

    graphs = get_graph_names(metadata_path)
    if graph_name not in graphs:
        print("Graph [{}] not known. The available ones are {}".format(
            task, graphs
        ))
        sys.exit(1)

    if task == "load":
        libraries = get_graph_libraries_names()
    elif task.startswith("first_order_walk"):
        libraries = get_first_order_walk_libraries_names()
    elif task.startswith("second_order_walk"):
        libraries = get_second_order_walk_libraries_names()
    else:
        print("Task [{}] not known. The available ones are {}".format(
            task, list(TASKS.keys())))
        sys.exit(1)

    if library not in libraries:
        if task != "load":
            print("Library [{}] not known. The available ones are {}".format(
                library, libraries))
            sys.exit(1)
        return

    graph_data = get_graph_data_from_graph_name(metadata_path, graph_name)

    TASKS[task](
        library=library,
        graph_name=graph_name,
        repository=graph_data["repository"],
        version=graph_data["version"],
        root=root,
        seconds=seconds
    )


def list_entrypoint(root, metadata_path, args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "topic", type=str, help="What you want to list (graphs, libraries, tasks)")
    topic = vars(parser.parse_args(args))["topic"]

    if topic not in LISTS:
        print("The topic {} is not known. The available ones are {}".format(
            topic, list(LISTS.keys())))
        sys.exit(1)

    values = LISTS[topic](metadata_path)
    print(json.dumps(values))
    sys.exit(0)


TASKS = {
    "load": bench_load_graph,
    "first_order_walk": bench_first_order_walks,
    "second_order_walk": lambda **x: bench_second_order_walks(**x, p=2.0, q=2.0),
    # "second_order_walk_only_q": lambda **x: bench_second_order_walks(**x, p=1.0, q=2.0),
    # "second_order_walk_only_p": lambda **x: bench_second_order_walks(**x, p=2.0, q=1.0),
}
LISTS = {
    "graphs": get_graph_names,
    "graph_libraries": lambda _: get_graph_libraries_names(),
    "first_order_walk": lambda _: get_first_order_walk_libraries_names(),
    "second_order_walk": lambda _: get_second_order_walk_libraries_names(),
    "libraries": lambda _: list(set(get_graph_libraries_names()) | set(get_first_order_walk_libraries_names()) | set(get_second_order_walk_libraries_names())),
    "tasks": lambda _: list(TASKS.keys())
}
SUB_COMMANDS = {
    "run": run_entrypoint,
    "list": list_entrypoint,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Main entrypoint for benchmarking")
    parser.add_argument("subcommand", type=str,
                        help="Which subcommand to execute")
    parser.add_argument("-m", "--metadata", type=str,
                        help="Path to where to load the experiments metadata", default="./graphs.json")
    parser.add_argument("-r", "--root", type=str,
                        help="Path to where to load the experiments metadata", default="./graphs")

    values, arguments_left = parser.parse_known_args(sys.argv[1:])
    subcommand, metadata_path, root = values.subcommand, values.metadata, values.root

    if subcommand not in SUB_COMMANDS:
        print("Subcommand {} not known. The available ones are : {}".format(
            subcommand, list(SUB_COMMANDS.keys())))
        sys.exit(1)

    if not os.path.exists(metadata_path):
        print("The metadata file {} does not exists.".format(metadata_path))
        sys.exit(1)

    SUB_COMMANDS[subcommand](root, metadata_path, arguments_left)
