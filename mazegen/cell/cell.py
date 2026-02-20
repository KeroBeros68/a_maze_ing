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
    maze generation. The locked flag can prevent wall modifications.

    Attributes:
        __wall: 4-bit integer representing walls (0xF = all walls,
        0x0 = no walls)
        __visited: Boolean indicating if cell was visited during generation
        __locked: Boolean indicating if cell is locked
                            (wall modifications prevented)
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
        self.__x: int = x
        self.__y: int = y
        self.__visited: bool = False
        self.__visited_since: int = 0
        self.__locked: bool = False
        self.__lock_code: str = " "
        self.__is_entry: bool = False
        self.__is_exit: bool = False

    def remove_cell_wall(self, wall: Wall) -> None:
        """Remove a wall from the cell using bitwise AND operation.

        Args:
            wall: Wall enum value (NORTH, EAST, SOUTH, or WEST)
        """
        self.__wall &= ~wall

    @property
    def wall(self) -> int:
        """Get the wall configuration of this cell.

        Returns:
            int: 4-bit integer where each bit represents a wall
        """
        return self.__wall

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def visited(self) -> bool:
        """Check if this cell has been visited.

        Returns:
            bool: True if cell was visited during maze generation
        """
        return self.__visited

    @visited.setter
    def visited(self, value: bool) -> None:
        """Mark the cell as visited or unvisited.

        Args:
            value: Whether the cell is visited
        """
        self.__visited = value

    @property
    def visited_since(self) -> int:
        return self.__visited_since

    @visited_since.setter
    def visited_since(self, value: int) -> None:
        self.__visited_since = value

    @property
    def locked(self) -> bool:
        """Check if this cell is locked.

        Returns:
            bool: True if cell is locked (wall modifications prevented)
        """
        return self.__locked

    @locked.setter
    def locked(self, value: bool) -> None:
        """Lock or unlock this cell.

        Args:
            value: Whether the cell is locked
        """
        self.__locked = value

    @property
    def lock_code(self) -> str:
        if self.__locked is False:
            return " "
        else:
            return self.__lock_code

    @lock_code.setter
    def lock_code(self, code: str) -> None:
        if code != " ":
            self.__locked = True
            self.__lock_code = code
        else:
            self.__locked = False
            self.__lock_code = " "

    @property
    def is_entry(self) -> bool:
        return self.__is_entry

    @is_entry.setter
    def is_entry(self, value: bool) -> None:
        self.__is_entry = value

    @property
    def is_exit(self) -> bool:
        return self.__is_exit

    @is_exit.setter
    def is_exit(self, value: bool) -> None:
        self.__is_exit = value

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

    cell.remove_cell_wall(Wall.EAST)
    print("Cell - East wall removed,  expected: 13, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.NORTH)
    print("Cell - North wall removed, expected: 14, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.SOUTH)
    print("Cell - South wall removed, expected: 11, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.WEST)
    print("Cell - West walls removed, expected:  7, actual:", cell)

    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.SOUTH)
    cell.remove_cell_wall(Wall.WEST)
    cell.remove_cell_wall(Wall.NORTH)
    cell.remove_cell_wall(Wall.EAST)
    print("Cell - All walls removed,  expected:  0, actual:", cell)

    print("\n==== Remove multiple Wall Test =====")
    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.SOUTH)
    cell.remove_cell_wall(Wall.WEST)
    print(
        "Cell - South and West walls removed, expected:  0011, actual:", cell
    )

    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.EAST)
    cell.remove_cell_wall(Wall.WEST)
    print(
        "Cell - East and West walls removed,  expected:  0101, actual:", cell
    )

    cell = Cell(0, 0)
    cell.remove_cell_wall(Wall.NORTH)
    cell.remove_cell_wall(Wall.EAST)
    print(
        "Cell - South and West walls removed, expected:  1100, actual:", cell
    )

    print("\n==== Visited Wall Test =====")
    cell = Cell(0, 0)
    print("Cell - Not visited, actual:", cell)
    cell.visited = True
    print("Cell - Visited, actual:", cell)
