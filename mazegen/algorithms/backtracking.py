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

    def generate(self, maze: Maze, entry_x: int, entry_y: int) -> Maze:
        """Generate a maze using the backtracking algorithm.

        Args:
            maze: Maze object to generate
            entry_x: Starting X coordinate
            entry_y: Starting Y coordinate

        Returns:
            Maze: The modified maze with passages carved by the algorithm
        """
        stack = [(entry_x, entry_y)]

        while stack:
            x1, y1 = stack[len(stack) - 1]
            maze.maze_grid[y1][x1].visit(True)
            try:
                target = self.valid_target(x1, y1, maze)
                x2, y2 = target
                maze = self.remove_wall(x1, y1, x2, y2, maze)
                x1, y1 = x2, y2
                stack.append((x1, y1))
            except Exception:
                stack.pop()
        return maze


if __name__ == "__main__":
    maze = Maze(10, 10, (5, 0), (9, 9))
    maze.init_grid()
    x, y = maze.entry
    random.seed(42)
    algorithm = BacktrackingAlgorithm()
    maze = algorithm.generate(maze, x, y)
    print(maze)
