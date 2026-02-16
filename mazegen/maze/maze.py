"""Maze grid structure and visualization.

This module defines the Maze class that represents the complete maze structure,
including all cells, dimensions, and entry/exit points. It handles grid
initialization and text-based visualization.
"""

from typing import Optional, Tuple
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
        self.__active_cell: Optional[Tuple[int, int]] = None
        self.__done_gen: bool = False
        self.__restart: bool = False  #Logique à déplacer dans controler

    @property
    def restart(self) -> bool:
        return self.__restart

    @restart.setter
    def restart(self, value: bool) -> None:
        self.__restart = value

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

    @property
    def active_cell(self) -> Optional[Tuple[int, int]]:
        """Get the currently active cell coordinates.

        Returns:
            Optional[Tuple[int, int]]: Coordinates (x, y) of the active cell,
            or None if no cell is active
        """
        return self.__active_cell

    @active_cell.setter
    def active_cell(self, value: Optional[Tuple[int, int]]) -> None:
        """Set the currently active cell coordinates.

        Args:
            value: Tuple (x, y) for the active cell coordinates,
            or None to clear
        """
        self.__active_cell = value

    @property
    def done_gen(self) -> bool:
        """Check if maze generation is complete.

        Returns:
            bool: True if generation has finished
        """
        return self.__done_gen

    @done_gen.setter
    def done_gen(self, value: bool) -> None:
        """Mark generation as complete or incomplete.

        Args:
            value: Whether generation is complete
        """
        self.__done_gen = value

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
        for row in self.maze_grid:
            for cell in row:
                coord_cell = (cell.x, cell.y)
                if coord_cell == self.entry:
                    cell.is_entry = True
                elif coord_cell == self.exit:
                    cell.is_exit = True

    def __str__(self) -> str:
        """Return a text-based visualization of the maze.

        Displays the maze grid with hexadecimal representation of cell walls.
        Each cell's wall state is shown as a single hexadecimal digit.

        Returns:
            str: Multi-line string representing the maze grid, with cells
                 separated by spaces and rows separated by newlines
        """

        result = []
        for y, row in enumerate(self.maze_grid):
            row_str = []
            for x, cell in enumerate(row):
                cell_view = cell.view_cell()
                row_str.append(cell_view)
            result.append("".join(row_str))
        return "\n".join(result)

    def __len__(self) -> int:
        return self.__width * self.__height


if __name__ == "__main__":
    maze = Maze(10, 10, (0, 0), (1, 1))
    maze.init_grid()
    print(maze)
    maze.maze_grid[1][0].remove_wall(Wall.EAST)
    print(maze.maze_grid[1][0])
    print(maze)
