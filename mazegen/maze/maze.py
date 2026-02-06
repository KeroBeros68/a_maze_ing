from typing import Tuple
from mazegen.utils.utils import Wall
from mazegen.cell.cell import Cell


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
    ):
        self.maze_grid: list[list[Wall]] = []
        self.__width: int = width
        self.__height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def init_grid(self):
        self.maze_grid = [
            [Cell(x, y) for x in range(self.__width)]
            for y in range(self.__height)
        ]

    def __str__(self) -> str:
        BLUE = "\033[94m"
        ORANGE = "\033[93m"
        RESET = "\033[39m"

        result = []
        for y, row in enumerate(self.maze_grid):
            row_str = []
            for x, cell in enumerate(row):
                cell_view = cell.view_cell()

                if (x, y) == self.entry:
                    cell_view = f"{BLUE}{cell.view_cell()}{RESET}"
                elif (x, y) == self.exit:
                    cell_view = f"{ORANGE}{cell.view_cell()}{RESET}"

                row_str.append(cell_view)
            result.append(" ".join(row_str))
        return "\n".join(result)

    # def __str__(self) -> str:
    #     BLUE = "\033[94m"
    #     ORANGE = "\033[93m"
    #     RESET = "\033[39m"

    #     result = []
    #     for y, row in enumerate(self.maze_grid):
    #         row_str = ["", "", ""]
    #         for x, cell in enumerate(row):
    #             cell_view = cell.view_cell()
    #             for i in range(3):
    #                 row_str[i] += cell_view[i]
    #         for ra in row_str:
    #             print(ra)
    #         # print("\n-----------------------------------")
    #     return ""


if __name__ == "__main__":
    maze = Maze(10, 10, (0, 0), (1, 1))
    maze.init_grid()
    print(maze)
    maze.maze_grid[1][0].remove_wall(Wall.EAST)
    print(maze.maze_grid[1][0])
    print(maze)
