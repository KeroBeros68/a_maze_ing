"""Maze grid structure and visualization.

This module defines the Maze class that represents the complete maze structure,
including all cells, dimensions, and entry/exit points. It handles grid
initialization and text-based visualization.
"""

from typing import Tuple
from mazegen.utils.utils import Wall
from mazegen.cell.cell import Cell


class Maze:
    """A maze grid consisting of cells with walls.

    This class represents the entire maze structure, managing:
    - A 2D grid of Cell objects
    - Maze dimensions (width and height)
    - Entry and exit point coordinates
    - Text-based visualization with colored entry/exit points

    Attributes:
        maze_grid: 2D list of Cell objects representing the maze
        __width: Width (number of columns) of the maze
        __height: Height (number of rows) of the maze
        entry: Tuple (x, y) for the entry point
        exit: Tuple (x, y) for the exit point
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
    ):
        """Initialize a maze with given dimensions and entry/exit points.

        Args:
            width: Width of the maze (number of columns)
            height: Height of the maze (number of rows)
            entry: Tuple (x, y) specifying the entry point coordinates
            exit: Tuple (x, y) specifying the exit point coordinates
        """
        self.maze_grid: list[list[Cell]] = []
        self.__width: int = width
        self.__height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit

    @property
    def width(self) -> int:
        """Get the width of the maze.

        Returns:
            int: Number of columns in the maze
        """
        return self.__width

    @property
    def height(self) -> int:
        """Get the height of the maze.

        Returns:
            int: Number of rows in the maze
        """
        return self.__height

    def init_grid(self) -> None:
        """Initialize the maze grid with Cell objects.

        Creates a 2D grid of Cell objects with dimensions matching
        the maze width and height. Each cell is initialized with its
        coordinates and all walls intact.
        """
        self.maze_grid = [
            [Cell(x, y) for x in range(self.__width)]
            for y in range(self.__height)
        ]

    def __str__(self) -> str:
        """Return a text-based visualization of the maze.

        Displays the maze grid with hexadecimal representation of cell walls.
        Each cell's wall state is shown as a single hexadecimal digit.

        Returns:
            str: Multi-line string representing the maze grid, with cells
                 separated by spaces and rows separated by newlines
        """

#        GREEN = "\033[0;1;38;2;0;191;95m"
#        BLUE = "\033[1;5;103;94m"
#        ORANGE = "\033[1;5;104;93m"
#        RESET = "\033[0;1;92m"

        result = []
        for y, row in enumerate(self.maze_grid):
            row_str = []
            for x, cell in enumerate(row):
                cell_view = f"{cell.view_cell()}"
#                if (x, y) == self.entry:
#                    cell_view = f"{BLUE}{cell.view_cell()}{RESET}"
#                elif (x, y) == self.exit:
#                    cell_view = f"{ORANGE}{cell.view_cell()}{RESET}"
#                else:
#                    cell_view = f"{GREEN}{cell.view_cell()}{RESET}"
                row_str.append(cell_view)
            result.append("".join(row_str))
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
