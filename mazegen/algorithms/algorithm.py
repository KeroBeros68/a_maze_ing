"""Abstract interface for maze generation algorithms.

This module defines the MazeAlgorithm abstract base class that all
maze generation algorithms must implement, enabling the Open/Closed
Principle by allowing new algorithms to be added without modifying
existing code.
"""

from abc import ABC, abstractmethod
from mazegen.maze.maze import Maze
from mazegen.utils.utils import Direction, Wall
from typing import Tuple, Generator
import random


class MazeAlgorithm(ABC):
    """Abstract base class for maze generation algorithms.

    This interface defines the contract that all maze generation
    algorithms must follow. Implementing this allows the MazeGenerator
    to remain open for extension without modification.

    Methods:
        generate: Abstract method to generate a maze
    """

    @abstractmethod
    def generate(
        self, maze: Maze, entry_x: int, entry_y: int, animate: bool = False
    ) -> Generator[Maze, None, None]:
        """Generate a maze starting from entry coordinates.

        Args:
            maze: The Maze object to generate
            entry_x: X coordinate of the entry point
            entry_y: Y coordinate of the entry point
            animate: If True, yields maze state after each step.
                    If False, yields only the final completed maze.

        Returns:
            Generator yielding Maze states. When animate=False, yields only
            the final completed maze state.

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        pass

    def valid_target(self, x: int, y: int, maze: Maze) -> Tuple[int, int]:
        """Find a random unvisited neighbor of the current cell.

        Checks all four adjacent cells (North, South, East, West) and
        returns a random choice from unvisited neighbors that are within
        maze bounds.

        Args:
            x: Current cell X coordinate
            y: Current cell Y coordinate
            maze: Maze object containing grid and dimensions

        Returns:
            Tuple[int, int]: Coordinates (x, y) of a random valid target cell

        Raises:
            IndexError: If no valid targets are available
            (all neighbors visited)
        """
        target = [
            (x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]

        valid_target = [
            (vx, vy)
            for vx, vy in target
            if 0 <= vx < maze.width
            and 0 <= vy < maze.height
            and not maze.maze_grid[vy][vx].visited
            and maze.maze_grid[vy][vx].locked == False
        ]

        return random.choice(valid_target)

    def remove_wall(
        self, x: int, y: int, x1: int, y1: int, maze: Maze
    ) -> Maze:
        """Remove walls between two adjacent cells to create a passage.

        Determines the direction from current cell to target cell and removes
        the corresponding wall from both cells. This creates a passage between
        the two cells.

        Args:
            x: Current cell X coordinate
            y: Current cell Y coordinate
            x1: Target cell X coordinate
            y1: Target cell Y coordinate
            maze: Maze object containing the grid to modify

        Returns:
            Maze: The modified maze with walls removed
        """
        if x + 1 == x1:
            maze.maze_grid[y][x].remove_cell_wall(Wall.EAST)
            maze.maze_grid[y1][x1].remove_cell_wall(
                Direction.EAST.opposite.wall)
        if x - 1 == x1:
            maze.maze_grid[y][x].remove_cell_wall(Wall.WEST)
            maze.maze_grid[y1][x1].remove_cell_wall(
                Direction.WEST.opposite.wall)
        if y + 1 == y1:
            maze.maze_grid[y][x].remove_cell_wall(Wall.SOUTH)
            maze.maze_grid[y1][x1].remove_cell_wall(
                Direction.SOUTH.opposite.wall)
        if y - 1 == y1:
            maze.maze_grid[y][x].remove_cell_wall(Wall.NORTH)
            maze.maze_grid[y1][x1].remove_cell_wall(
                Direction.NORTH.opposite.wall)
        return maze
