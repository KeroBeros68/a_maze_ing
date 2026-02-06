"""Maze generation orchestration.

This module provides the main interface for generating mazes using
the backtracking algorithm with a given configuration.
"""

import random
from mazegen.algorithms.backtracking import backtrack
from mazegen.maze.maze import Maze
from mazegen.utils.model import ConfigModel


class MazeGenerator():
    """Generate a maze using the backtracking algorithm.

    This class orchestrates the maze generation process by:
    - Initializing maze dimensions and entry/exit points
    - Creating the maze grid structure
    - Applying the backtracking generation algorithm
    - Managing random seed for reproducible generation

    Attributes:
        __width: Width of the maze
        __height: Height of the maze
        __entry: Tuple of (x, y) coordinates for maze entry point
        __exit: Tuple of (x, y) coordinates for maze exit point
        __seed: Random seed for reproducible maze generation
        maze: The generated Maze object
    """

    def __init__(self, config: ConfigModel):
        """Initialize MazeGenerator with configuration parameters.

        Args:
            config: ConfigModel instance containing:
                - WIDTH: Maze width
                - HEIGHT: Maze height
                - ENTRY: Entry coordinates (x, y)
                - EXIT: Exit coordinates (x, y)
                - SEED: Random seed for generation
        """
        self.__width = config.WIDTH
        self.__height = config.HEIGHT
        self.__entry = config.ENTRY
        self.__exit = config.EXIT
        self.__seed = config.SEED
        self.maze: Maze = Maze(self.__width, self.__height, self.__entry,
                               self.__exit)

    def generate_maze(self) -> Maze:
        """Generate a maze using the backtracking algorithm.

        Creates a maze grid, initializes all cells, sets the random seed,
        and applies the backtracking algorithm starting from the entry point.

        Returns:
            Maze: The generated maze object with walls removed according
                  to the backtracking algorithm
        """
        self.maze.init_grid()
        random.seed(self.__seed)
        # Maze generation algorithm
        x, y = self.__entry
        self.maze = backtrack(self.maze, x, y)
        return self.maze
