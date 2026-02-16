from typing import Iterable
from mazegen.maze.maze import Maze
from mazegen.stamp.StampConsts import FortyTwo

class Stamp:
    def __init__(self, maze: Maze) -> None:
        self.__maze = maze

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

    def add_stamp(self) -> None:
        x, y = int(self.__maze.width / 2 - 3), 0
        self.add_stamp_block(x, y, FortyTwo.VANILLA)
        x, y = int(self.__maze.width / 2), int(self.__maze.height / 2)
        self.add_stamp_block(x, y, FortyTwo.SMALL)
        x, y = int(self.__maze.width / 2 - 13), 5
        self.add_stamp_block(x, y, FortyTwo.MEDIUM)
        x, y = int(self.__maze.width - 17), int(self.__maze.height - 15)
        self.add_stamp_block(x, y, FortyTwo.LARGE)
