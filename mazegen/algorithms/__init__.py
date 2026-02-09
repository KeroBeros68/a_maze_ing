"""Maze generation algorithms package.

This package contains implementations of various maze generation algorithms.
Algorithms are accessed through the AlgorithmFactory for extensibility.
"""

from mazegen.algorithms.algorithm import MazeAlgorithm
from mazegen.algorithms.backtracking import BacktrackingAlgorithm
from mazegen.algorithms.factory import AlgorithmFactory

__all__ = [
    "MazeAlgorithm",
    "BacktrackingAlgorithm",
    "AlgorithmFactory",
]
