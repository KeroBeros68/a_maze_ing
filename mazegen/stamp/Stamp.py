from typing import Iterable, Tuple, List
from mazegen.maze.maze import Maze
from mazegen.stamp.StampConsts import FortyTwo
import random


class Stamp:
    def __init__(self, maze: Maze, logo_type: str) -> None:
        self.__maze = maze
        self.__logo_type = logo_type

    def add_stamp_block(
                self,
                x: int,
                y: int,
                block: str | Iterable[str],
            ) -> None:
        if isinstance(block, str):
            lines = block.splitlines()
        else:
            lines = list(block)
        for dy, line in enumerate(lines):
            if not line:
                continue
            gy = y + dy
            gx = x
            for ch in line:
                if ch != " ":
                    self.__maze.maze_grid[gy][gx].locked = True
                    self.__maze.maze_grid[gy][gx].lock_code = ch
                gx += 1

    def stamp_bsq(self) -> Tuple[int, int, int]:
        xdim = self.__maze.width
        ydim = self.__maze.height
        xin, yin = self.__maze.entry
        xout, yout = self.__maze.exit
        win = 0
        best: List[Tuple[int, int, int]] = []
        matrix: List[List[int]] = [[0] * xdim for _ in range(ydim)]

        for y in range(ydim):
            for x in range(xdim):
                if (x == xin and y == yin) or (x == xout and y == yout):
                    matrix[y][x] = 0
                else:
                    l_cell = matrix[y][x - 1] if x > 0 else 0
                    u_cell = matrix[y - 1][x] if y > 0 else 0
                    ul_cell = matrix[y - 1][x - 1] if (x > 0 and y > 0) else 0
                    matrix[y][x] = min(l_cell, u_cell, ul_cell) + 1
                    value = matrix[y][x]
                    if value > win and win < 18:
                        win = value
                        best = [(x - (win - 1), y - (win - 1), win)]
                    elif value == win and win > 0:
                        best.append((x - (win - 1), y - (win - 1), win))
                    elif value >= 18:
                        best.append((x - (value - 1), y - (value - 1), value))

        if win == 0:
            return 0, 0, 0

        idx = random.randrange(len(best))
        return best[idx]

    def add_stamp(self) -> None:
        x, y, bsq_size = self.stamp_bsq()
        if self.__logo_type == "vanilla":
            logo = FortyTwo.VANILLA
        else:
            if bsq_size >= len(FortyTwo.LARGE):
                logo = FortyTwo.LARGE
            elif bsq_size >= len(FortyTwo.MEDIUM):
                logo = FortyTwo.MEDIUM
            else:
                logo = FortyTwo.SMALL
        logo_size = len(logo)
        diff_size = bsq_size - logo_size + 1
        x_var = random.randrange(diff_size)
        y_var = random.randrange(diff_size)
        self.add_stamp_block(x + x_var, y + y_var, logo)


"""Tests
        print(x, y, size, seed)
        sys.exit(0)
        x, y = int(self.__maze.width / 2 - 3), 0
        self.add_stamp_block(x, y, FortyTwo.VANILLA)
        x, y = int(self.__maze.width / 2), int(self.__maze.height / 2)
        self.add_stamp_block(x, y, FortyTwo.SMALL)
        x, y = int(self.__maze.width / 2 - 13), 5
        self.add_stamp_block(x, y, FortyTwo.MEDIUM)
        x, y = int(self.__maze.width - 17), int(self.__maze.height - 15)
        self.add_stamp_block(x, y, FortyTwo.LARGE)
"""
