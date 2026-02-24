"""Maze generation orchestration.

This module provides the main interface for generating mazes using
configurable algorithms. The MazeGenerator remains open for extension
through the algorithm factory pattern.
"""

import random
import uuid
from sys import stderr
from typing import Generator
from mazegen.maze.maze import Maze
from mazegen.stamp.Stamp import Stamp
from mazegen.algorithms.factory import AlgorithmFactory
from mazegen.model import ConfigModel


class MazeGenerator:
    """Generate a maze using a configurable algorithm.

    This class orchestrates the maze generation process by:
    - Initializing maze dimensions and entry/exit points
    - Creating the maze grid structure
    - Selecting and applying the specified generation algorithm
    - Managing random seed for reproducible generation

    Attributes:
        __width: Width of the maze
        __height: Height of the maze
        __entry: Tuple of (x, y) coordinates for maze entry point
        __exit: Tuple of (x, y) coordinates for maze exit point
        __seed: Random seed for reproducible maze generation
        __algorithm_name: Name of the algorithm to use
        maze: The generated Maze object
    """

    def __init__(self, config: ConfigModel):
        """Initialize MazeGenerator with configuration.

        Args:
            config: ConfigModel instance with all maze generation settings

        Raises:
            ValueError: If the specified algorithm is not registered
        """
        self.__width = config.WIDTH
        self.__height = config.HEIGHT
        self.__entry = config.ENTRY
        self.__exit = config.EXIT
        self.__output_file = config.OUTPUT_FILE
        self.__seed = config.SEED
        self.__algorithm_name = config.ALGORITHM
        self.__perfect = config.PERFECT
        self.__mode_gen = config.MODE_GEN
        self.__stamp_type = config.STAMP_TYPE
        self.maze: Maze = Maze(
            self.__width, self.__height, self.__entry, self.__exit,
            self.__perfect)
        self.stamp: Stamp = Stamp(self.maze, self.__stamp_type)

    def generate_maze(self) -> Generator[Maze, None, None]:
        """Generate a maze using the configured algorithm.

        Creates a maze grid, initializes all cells, sets the random seed,
        and applies the selected algorithm starting from the entry point.

        Returns:
            Generator yielding Maze states. When mode_gen is 'animated',
            yields intermediate states. Otherwise, yields only the final
            completed maze.

        Raises:
            ValueError: If the algorithm is not found
        """
        self.maze.init_grid()
        if self.__seed is None:
            self.generate_new_seed()
        random.seed(self.__seed)
        self.stamp.add_stamp()

        # Get algorithm from factory
        try:
            algorithm = AlgorithmFactory.create(self.__algorithm_name)
        except ValueError as e:
            stderr.write(f"Error: {e}\n")
            raise

        x, y = self.__entry
        animate = self.__mode_gen == "animated"
        return algorithm.generate(self.maze, x, y, animate=animate)

    def create_output_file(self) -> None:
        """Write the generated maze to an output file.

        Saves the maze visualization to a text file along with entry and exit
        coordinates in CSV format (x,y). Creates or overwrites the output file
        specified in the configuration.

        Returns:
            None

        Raises:
            IOError: If the file cannot be written
            (caught and printed as error)
        """
        x, y = self.__entry
        x1, y1 = self.__exit
        try:
            with open(self.__output_file, "w") as file:
                file.write(self.maze.__str__())
                file.write("\n\n")
                file.write(f"{x},{y}\n")
                file.write(f"{x1},{y1}\n")
                file.write(self.maze.shortest_path)
        except (FileNotFoundError, PermissionError) as e:
            stderr.write(f"Error writing file: {str(e)}\n")

    def generate_new_seed(self) -> None:
        """Generate a random seed as a hex string."""
        self.__seed = uuid.uuid4().hex

    def get_seed(self) -> str | None:
        return self.__seed
