"""Backtracking maze generation algorithm.

This module implements the depth-first search backtracking algorithm
for generating perfect mazes. It carves passages by removing walls
between adjacent unvisited cells.
"""

from typing import Generator
from mazegen.maze.maze import Maze
from mazegen.algorithms.algorithm import MazeAlgorithm
from mazegen.algorithms.unperfect import UnPerfect


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
        stack = [(entry_x, entry_y, 0)]

        def _generate() -> Generator[Maze, None, None]:
            """Internal generator that yields maze states."""
            nonlocal maze
            maze.gen_step = 1
            while stack:
                x1, y1, _ = stack[len(stack) - 1]
                maze.maze_grid[y1][x1].visited = True
                if animate:
                    maze.active_cell = stack[len(stack) - 1]

                try:
                    target = self.valid_target(x1, y1, maze)
                    x2, y2 = target
                    maze = self.remove_wall(x1, y1, x2, y2, maze)
                    if animate:
                        tx, ty = target
                        maze.active_cell = tx, ty, 0
                        yield maze
                    x1, y1 = x2, y2
                    stack.append((x1, y1, 0))
                except Exception:
                    stack.pop()
                    if animate:
                        try:
                            maze.active_cell = stack[len(stack) - 1]
                        except IndexError:
                            maze.active_cell = (entry_x, entry_y, 0)
                        yield maze

            maze.gen_step = 2
            if maze.perfect is False:
                algo = UnPerfect()
                yield from algo.generate(maze, 0, 0, animate)
            else:
                maze.gen_step = 3

            # Always yield the final maze
            yield maze

        return _generate()
