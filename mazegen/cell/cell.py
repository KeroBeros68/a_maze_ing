"""Cell representation in a maze.

This module defines a Cell class that represents a single cell in a maze grid.
Each cell tracks its walls (North, East, South, West) using bit flags and
whether it has been visited during maze generation.
"""

from mazegen.utils.utils import Wall


class Cell:
    """A single cell in a maze grid.

    Each cell has four walls (North, East, South, West) represented as bits
    in a 4-bit integer. Walls can be removed to create passages between cells.
    The visited flag tracks whether the cell has been processed during
    maze generation.

    Attributes:
        __wall: 4-bit integer representing walls (0xF = all walls,
        0x0 = no walls)
        visited: Boolean indicating if cell was visited during generation
        __x: X coordinate of cell in maze grid
        __y: Y coordinate of cell in maze grid
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell at the given coordinates.

        Args:
            x: X coordinate in the maze grid
            y: Y coordinate in the maze grid
        """
        self.__wall: int = 0xF
        self.visited: bool = False
        self.__x: int = x
        self.__y: int = y

    def remove_wall(self, wall: Wall) -> None:
        """Remove a wall from the cell using bitwise AND operation.

        Args:
            wall: Wall enum value (NORTH, EAST, SOUTH, or WEST)
        """
        self.__wall &= ~wall

    def visit(self, is_visited: bool) -> None:
        """Mark cell as visited or unvisited.

        Args:
            is_visited: True to mark cell as visited, False otherwise
        """
        self.visited = is_visited

    def __str__(self) -> str:
        """Return detailed string representation of the cell.

        Returns:
            str: Cell information including wall state, binary representation,
                 visited status, and maze coordinates
        """
        return (
            f"Cell: {self.__wall:2}  {self.__wall:04b}  {self.__wall:X}"
            f" is visited: {self.visited} "
            f"position in maze: {self.__x}, {self.__y}"
        )

    def view_cell(self) -> str:
        """Return hexadecimal representation of the cell's wall state.

        Returns:
            str: Hexadecimal value representing the current wall configuration
        """
        wall_hex = f"{self.__wall:X}"

        return f"{wall_hex}"


if __name__ == "__main__":
    print("==== Remove Wall Test =====")

    cell = Cell(0, 0)
    print("Default cell, expected: 15, actual:", cell)

    cell.remove_wall(Wall.EAST)
    print("Cell - East wall removed,  expected: 13, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_wall(Wall.NORTH)
    print("Cell - North wall removed, expected: 14, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_wall(Wall.SOUTH)
    print("Cell - South wall removed, expected: 11, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_wall(Wall.WEST)
    print("Cell - West walls removed, expected:  7, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_wall(Wall.SOUTH)
    cell.remove_wall(Wall.WEST)
    cell.remove_wall(Wall.NORTH)
    cell.remove_wall(Wall.EAST)
    print("Cell - All walls removed,  expected:  0, actual:", cell)

    print("\n==== Remove multiple Wall Test =====")
    cell = Cell(0, 0)
    cell.remove_wall(Wall.SOUTH)
    cell.remove_wall(Wall.WEST)
    print(
        "Cell - South and West walls removed, expected:  0011, actual:", cell
    )

    cell = Cell(0, 0)
    cell.remove_wall(Wall.EAST)
    cell.remove_wall(Wall.WEST)
    print(
        "Cell - East and West walls removed,  expected:  0101, actual:", cell
    )

    cell = Cell(0, 0)
    cell.remove_wall(Wall.NORTH)
    cell.remove_wall(Wall.EAST)
    print(
        "Cell - South and West walls removed, expected:  1100, actual:", cell
    )

    print("\n==== Visited Wall Test =====")
    cell = Cell(0, 0)
    print("Cell - Not visited, actual:", cell)
    cell.visit(True)
    print("Cell - Visited, actual:", cell)
