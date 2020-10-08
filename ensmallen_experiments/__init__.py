"""Module to reproduce the Ensmallen library experiments."""
import silence_tensorflow.auto
from .retrieve_graphs import retrieve_graphs

__all__ = [
    "retrieve_graphs",
]