"""Backtracking maze generation algorithm.

This module implements the depth-first search backtracking algorithm
for generating perfect mazes. It carves passages by removing walls
between adjacent unvisited cells.
"""

import random
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
    ):
        """Generate a maze using the backtracking algorithm.

        Args:
            maze: Maze object to generate
            entry_x: Starting X coordinate
            entry_y: Starting Y coordinate
            animate: If True, yields maze state at each step (for animation).
                    If False, returns completed maze after generation.

        Returns:
            If animate=False: Maze object with passages carved
            If animate=True: Generator yielding Maze states at each step
        """
        stack = [(entry_x, entry_y)]

        def _generate():
            """Internal generator that yields maze states."""
            nonlocal maze
            while stack:
                x1, y1 = stack[len(stack) - 1]
                maze.maze_grid[y1][x1].visit(True)
                yield maze

                try:
                    target = self.valid_target(x1, y1, maze)
                    x2, y2 = target
                    maze = self.remove_wall(x1, y1, x2, y2, maze)
                    yield maze
                    x1, y1 = x2, y2
                    stack.append((x1, y1))
                except Exception:
                    stack.pop()

        if animate:
            return _generate()
        else:
            # Run through all generations without yielding
            for final_maze in _generate():
                pass
            return final_maze


if __name__ == "__main__":
    maze = Maze(10, 10, (5, 0), (9, 9))
    maze.init_grid()
    x, y = maze.entry
    random.seed(42)
    algorithm = BacktrackingAlgorithm()
    maze = algorithm.generate(maze, x, y)
    print(maze)
