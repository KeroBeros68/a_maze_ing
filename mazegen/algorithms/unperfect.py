import math
import random
from typing import Generator
from mazegen.maze.maze import Maze
from mazegen.algorithms.algorithm import MazeAlgorithm


class UnPerfect(MazeAlgorithm):

    def generate(
        self, maze: Maze, entry_x: int, entry_y: int, animate: bool = False
    ) -> Generator[Maze, None, None]:

        def in_bounds(x: int, y: int) -> bool:
            return 0 <= x < maze.width and 0 <= y < maze.height

        def _generate() -> Generator[Maze, None, None]:
            nonlocal maze

            def count_openings(code: int) -> int:
                count = 0
                if not code & 1:
                    count += 1
                if not code & 2:
                    count += 1
                if not code & 3:
                    count += 1
                if not code & 4:
                    count += 1
                return count

            width = maze.width
            height = maze.height

            targets = int(math.sqrt(width * height)) * 3
            removed = 0
            candidates = []

            for y in range(height):
                for x in range(width):

                    if maze.maze_grid[y][x].locked:
                        continue

                    cell = f"{maze.maze_grid[y][x].view_cell()}"
                    code = int(cell, 16)
                    if x + 1 < width:
                        if not maze.maze_grid[y][x + 1].locked:
                            if code & 2:
                                candidates.append((x, y, x + 1, y, 2))
                    if y + 1 < height:
                        if not maze.maze_grid[y + 1][x].locked:
                            if code & 4:
                                candidates.append((x, y, x, y + 1, 4))

            random.shuffle(candidates)

            for x1, y1, x2, y2, code in candidates:

                if removed >= targets:
                    break

                c1 = maze.maze_grid[y1][x1]
                c2 = maze.maze_grid[y2][x2]

                if c1.locked or c2.locked:
                    continue
                if count_openings(int(f"{c1.view_cell()}", 16)) >= 2:
                    continue
                if count_openings(int(f"{c2.view_cell()}", 16)) >= 2:
                    continue

                maze = self.remove_wall(x1, y1, x2, y2, maze)
                removed += 1

                if animate:
                    maze.active_cell = (x1, y1, code)
                    yield maze

            maze.gen_step = 3
            yield maze

        return _generate()
