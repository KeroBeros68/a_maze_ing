"""Backtracking maze generation algorithm.

This module implements the depth-first search backtracking algorithm
for generating perfect mazes. It carves passages by removing walls
between adjacent unvisited cells.
"""

import random
from typing import Generator
from mazegen.maze.maze import Maze
from mazegen.algorithms.algorithm import MazeAlgorithm


class BacktrackingAlgorithm(MazeAlgorithm):
    """Backtracking algorithm implementation for maze generation.

    Uses depth-first search with a stack to carve passages through the maze.
    Starting from entry coordinates, recursively visits unvisited neighbors
    and removes walls between visited and current cells.
    """

    def generate(
        self, maze: Maze, entry_x: int, entry_y: int, animate: bool = False
    ) -> Generator[Maze, None, None]:
        """Generate a maze using the backtracking algorithm.

        Args:
            maze: Maze object to generate
            entry_x: Starting X coordinate
            entry_y: Starting Y coordinate
            animate: If True, yields maze state at each step (for animation).
                    If False, yields only the final completed maze.

        Returns:
            Generator yielding Maze states at each step.
        """
        stack = [(entry_x, entry_y)]

        def _generate() -> Generator[Maze, None, None]:
            """Internal generator that yields maze states."""
            nonlocal maze
            while stack:
                x1, y1 = stack[len(stack) - 1]
                maze.maze_grid[y1][x1].visited = True
                if animate:
                    maze.active_cell = stack[len(stack) - 1]

                try:
                    target = self.valid_target(x1, y1, maze)
                    x2, y2 = target
                    maze = self.remove_wall(x1, y1, x2, y2, maze)
                    if animate:
                        maze.active_cell = target
                        yield maze
                    x1, y1 = x2, y2
                    stack.append((x1, y1))
                except Exception:
                    stack.pop()
            # Always yield the final maze
            maze.done_gen = True
            yield maze

        return _generate()


if __name__ == "__main__":
    initial_maze = Maze(10, 10, (5, 0), (9, 9))
    initial_maze.init_grid()
    x, y = initial_maze.entry
    random.seed(42)
    algorithm = BacktrackingAlgorithm()
    generator = algorithm.generate(initial_maze, x, y)
    # Consume the generator to get the final maze
    final_maze: Maze = initial_maze
    for final_maze in generator:
        pass
    print(final_maze)
