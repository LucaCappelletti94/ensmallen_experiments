"""Run the experiments entire pipeline."""
from ensmallen_experiments import retrieve_graphs

if __name__ == "__main__":
    # First we retrieve and sanitize the graph
    retrieve_graphs("graphs.json")
    # Then we proceed with the benchmarks
    # TODO: benchmarks