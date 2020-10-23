"""Submodule with bench for the various libraries."""

from .bench_csrgraph import load_graph_csrgraph, execute_walks_csrgraph
from .bench_ensmallen import load_graph_ensmallen, execute_walks_ensmallen, load_graph_fast_ensmallen
from .bench_graph_embedding import execute_walks_graph_embedding
from .bench_igraph import load_graph_igraph, execute_first_order_walk_igraph
from .bench_networkx import load_graph_networkx
from .bench_node2vec import execute_walks_node2vec


libraries = {
    "CSRgraph": {
        "load_graph": load_graph_csrgraph,
        "first_order_walk": {
            "load_graph": "CSRgraph",
            "walk": execute_walks_csrgraph
        },
        "second_order_walk": {
            "load_graph": "CSRgraph",
            "walk": execute_walks_csrgraph
        }
    },
    "EnsmallenGraph": {
        "load_graph": load_graph_ensmallen,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph",
            "walk": execute_walks_ensmallen
        }
    },
    "FastEnsmallenGraph": {
        "load_graph": load_graph_fast_ensmallen,
        "first_order_walk": {
            "load_graph": "FastEnsmallenGraph",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "FastEnsmallenGraph",
            "walk": execute_walks_ensmallen
        }
    },
    "iGraph": {
        "load_graph": load_graph_igraph,
        "first_order_walk": {
            "load_graph": "iGraph",
            "walk": execute_first_order_walk_igraph
        },
    },
    "Networkx": {
        "load_graph": load_graph_networkx,
    },
    "GraphEmbedding": {
        "first_order_walk": {
            "load_graph": "Networkx",
            "walk": execute_walks_graph_embedding
        },
        "second_order_walk": {
            "load_graph": "Networkx",
            "walk": execute_walks_graph_embedding
        }
    },
    "Node2Vec": {
        "first_order_walk": {
            "load_graph": "Networkx",
            "walk": execute_walks_node2vec
        },
        "second_order_walk": {
            "load_graph": "Networkx",
            "walk": execute_walks_node2vec
        }
    },
}


__all__ = ["libraries"]
