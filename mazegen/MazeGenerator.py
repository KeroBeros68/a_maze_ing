"""Maze generation orchestration.

This module provides the main interface for generating mazes using
configurable algorithms. The MazeGenerator remains open for extension
through the algorithm factory pattern.
"""

import random
import uuid
from sys import stderr
from typing import Tuple, Optional, Generator
from mazegen.maze.maze import Maze
from mazegen.algorithms.factory import AlgorithmFactory


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

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: str,
        seed: Optional[str],
        algorithm: str,
        mode_gen: str,
    ):
        """Initialize MazeGenerator with configuration parameters.

        Args:
            width: Width of the maze
            height: Height of the maze
            entry: Entry coordinates as tuple (x, y)
            exit: Exit coordinates as tuple (x, y)
            output_file: Path to the output file
            seed: Random seed for reproducible generation (None for random)
            algorithm: Name of the algorithm to use (default: "backtracking")
            mode_gen: Generation mode ("normal" or "animated")

        Raises:
            ValueError: If the specified algorithm is not registered
        """
        self.__width = width
        self.__height = height
        self.__entry = entry
        self.__exit = exit
        self.__output_file = output_file
        self.__seed = seed
        self.__algorithm_name = algorithm
        self.__mode_gen = mode_gen
        self.maze: Maze = Maze(
            self.__width, self.__height, self.__entry, self.__exit
        )

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
                file.write(f"{x1},{y1}")
        except (FileNotFoundError, PermissionError) as e:
            stderr.write(f"Error writing file: {str(e)}\n")

    def generate_new_seed(self) -> None:
        """Generate a random seed as a hex string."""
        self.__seed = uuid.uuid4().hex
