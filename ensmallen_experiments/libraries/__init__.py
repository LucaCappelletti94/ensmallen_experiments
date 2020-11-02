"""Submodule with bench for the various libraries."""
from .bench_csrgraph import load_graph_csrgraph, execute_walks_csrgraph
from .bench_ensmallen import (
    load_graph_ensmallen,
    execute_walks_ensmallen,
    load_graph_fast_ensmallen,
    load_graph_ensmallen_5_percent_cache,
    load_graph_ensmallen_10_percent_cache,
    load_graph_ensmallen_15_percent_cache,
    load_graph_ensmallen_20_percent_cache,
    load_graph_ensmallen_25_percent_cache,
    load_graph_ensmallen_30_percent_cache,
    load_graph_ensmallen_35_percent_cache,
    load_graph_ensmallen_40_percent_cache,
    load_graph_ensmallen_45_percent_cache,
    load_graph_ensmallen_50_percent_cache,
    load_graph_ensmallen_55_percent_cache,
    load_graph_ensmallen_60_percent_cache,
    load_graph_ensmallen_65_percent_cache,
    load_graph_ensmallen_70_percent_cache,
    load_graph_ensmallen_75_percent_cache,
    load_graph_ensmallen_80_percent_cache,
    load_graph_ensmallen_85_percent_cache,
    load_graph_ensmallen_90_percent_cache,
    load_graph_ensmallen_95_percent_cache
)
from .bench_graph_embedding import execute_walks_graph_embedding
from .bench_igraph import load_graph_igraph, execute_first_order_walk_igraph
from .bench_networkx import load_graph_networkx
from .bench_node2vec import execute_walks_node2vec
from .bench_pecanpy import load_graph_pecanpy, execute_walks_pecanpy


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
    "EnsmallenGraph5PercentCache": {
        "load_graph": load_graph_ensmallen_5_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph5PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph5PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph10PercentCache": {
        "load_graph": load_graph_ensmallen_10_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph10PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph10PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph15PercentCache": {
        "load_graph": load_graph_ensmallen_15_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph15PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph15PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph20PercentCache": {
        "load_graph": load_graph_ensmallen_20_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph20PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph20PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph25PercentCache": {
        "load_graph": load_graph_ensmallen_25_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph25PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph25PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph30PercentCache": {
        "load_graph": load_graph_ensmallen_30_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph30PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph30PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph35PercentCache": {
        "load_graph": load_graph_ensmallen_35_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph35PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph35PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph40PercentCache": {
        "load_graph": load_graph_ensmallen_40_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph40PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph40PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph45PercentCache": {
        "load_graph": load_graph_ensmallen_45_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph45PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph45PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph50PercentCache": {
        "load_graph": load_graph_ensmallen_50_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph50PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph50PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph55PercentCache": {
        "load_graph": load_graph_ensmallen_55_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph55PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph55PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph60PercentCache": {
        "load_graph": load_graph_ensmallen_60_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph60PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph60PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph65PercentCache": {
        "load_graph": load_graph_ensmallen_65_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph65PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph65PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph70PercentCache": {
        "load_graph": load_graph_ensmallen_70_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph70PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph70PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph75PercentCache": {
        "load_graph": load_graph_ensmallen_75_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph75PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph75PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph80PercentCache": {
        "load_graph": load_graph_ensmallen_80_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph80PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph80PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph85PercentCache": {
        "load_graph": load_graph_ensmallen_85_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph85PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph85PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph90PercentCache": {
        "load_graph": load_graph_ensmallen_90_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph90PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph90PercentCache",
            "walk": execute_walks_ensmallen
        }
    },
    "EnsmallenGraph95PercentCache": {
        "load_graph": load_graph_ensmallen_95_percent_cache,
        "first_order_walk": {
            "load_graph": "EnsmallenGraph95PercentCache",
            "walk": execute_walks_ensmallen
        },
        "second_order_walk": {
            "load_graph": "EnsmallenGraph95PercentCache",
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
    "PecanPy": {
        "load_graph": load_graph_pecanpy,
        "first_order_walk": {
            "load_graph": "PecanPy",
            "walk": execute_walks_pecanpy
        },
        "second_order_walk": {
            "load_graph": "PecanPy",
            "walk": execute_walks_pecanpy
        }
    },
}


__all__ = ["libraries"]
