"""Maze generation package.

Provides the core maze generation functionality including algorithms,
cell structures, and maze grid management.

Modules:
    algorithms: Maze generation algorithms (backtracking, etc.)
    cell: Individual cell representation with wall management
    maze: Complete maze grid structure
    utils: Utility enumerations for walls and directions
    error: Exception classes for the mazegen package
"""

from . import utils, cell, algorithms
from .error import MazeError, StampError


__all__ = ["utils", "cell", "algorithms", "MazeError", "StampError"]
