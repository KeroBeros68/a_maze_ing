"""Prim's algorithm implementation for maze generation.

This module implements Prim's algorithm for generating perfect mazes.
It uses a frontier set approach to grow the maze from a starting point.

Classes:
    PrimAlgorithm: Implementation of Prim's maze generation algorithm
"""

import random
from typing import Generator
from mazegen.maze.maze import Maze
from mazegen.algorithms.algorithm import MazeAlgorithm
from mazegen.algorithms.unperfect import UnPerfect


class PrimAlgorithm(MazeAlgorithm):
    """Prim's algorithm implementation for maze generation.

    Uses a frontier-set approach to progressively expand the maze by
    connecting unvisited cells to the existing maze structure.
    Creates perfect mazes with guaranteed solution paths.
    """

    def generate(
        self, maze: Maze, entry_x: int, entry_y: int, animate: bool = False
    ) -> Generator[Maze, None, None]:
        """Generate a maze using Prim's algorithm.

        Args:
            maze: Maze object to generate
            entry_x: Starting X coordinate
            entry_y: Starting Y coordinate
            animate: If True, yields maze state at each step.
                    If False, yields only the final completed maze.

        Returns:
            Generator yielding Maze states at each step.
        """

        def in_bounds(x: int, y: int) -> bool:
            return 0 <= x < maze.width and 0 <= y < maze.height

        def neighbors(x: int, y: int) -> list[tuple[int, int]]:
            cand = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
            return [(nx, ny) for (nx, ny) in cand if in_bounds(nx, ny)]

        def _generate() -> Generator[Maze, None, None]:
            nonlocal maze
            maze.gen_step = 1

            maze.maze_grid[entry_y][entry_x].visited = True
            if animate:
                maze.active_cell = (entry_x, entry_y, 0)
                yield maze

            frontier: list[tuple[int, int]] = []
            in_frontier: set[tuple[int, int]] = set()

            def add_frontier(nx: int, ny: int) -> None:
                if (not maze.maze_grid[ny][nx].visited
                   and (nx, ny) not in in_frontier):
                    frontier.append((nx, ny))
                    in_frontier.add((nx, ny))

            for nx, ny in neighbors(entry_x, entry_y):
                add_frontier(nx, ny)

            while frontier:
                idx = random.randrange(len(frontier))
                x2, y2 = frontier.pop(idx)
                in_frontier.discard((x2, y2))

                if (maze.maze_grid[y2][x2].visited
                   or maze.maze_grid[y2][x2].locked is True):
                    continue

                visited_nbs = [(nx, ny) for (nx, ny) in neighbors(x2, y2)
                               if maze.maze_grid[ny][nx].visited]
                if not visited_nbs:
                    continue

                x1, y1 = random.choice(visited_nbs)

                maze = self.remove_wall(x1, y1, x2, y2, maze)
                maze.maze_grid[y2][x2].visited = True

                if animate:
                    maze.active_cell = (x2, y2, 0)
                    yield maze
                for nx, ny in neighbors(x2, y2):
                    add_frontier(nx, ny)

            maze.gen_step = 2
            if maze.perfect is False:
                algo = UnPerfect()
                yield from algo.generate(maze, 0, 0, animate)
            else:
                maze.gen_step = 3

            yield maze

        return _generate()
