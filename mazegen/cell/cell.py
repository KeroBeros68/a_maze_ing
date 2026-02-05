from ..utils import Wall, Direction


class Cell:
    def __init__(self):
        self.__wall: int = 0xF
        self.__visited: bool = False

    def remove_wall(self, wall: Wall):
        self.__wall &= ~wall

    def visit(self, is_visited: bool):
        self.__visited = is_visited

    def __str__(self):
        return (
            f"Cellule: {self.__wall:2}  {self.__wall:04b}  {self.__wall:X}"
            f" is visited: {self.__visited}"
        )


if __name__ == "__main__":
    print("==== Remove Wall Test =====")

    cell = Cell()
    print("Default cell, expected: 15, actual:", cell)

    cell.remove_wall(Wall.EAST)
    print("Cell - East wall removed,  expected: 13, actual:", cell)

    cell = Cell()
    cell.remove_wall(Wall.NORTH)
    print("Cell - North wall removed, expected: 14, actual:", cell)

    cell = Cell()
    cell.remove_wall(Wall.SOUTH)
    print("Cell - South wall removed, expected: 11, actual:", cell)

    cell = Cell()
    cell.remove_wall(Wall.WEST)
    print("Cell - West walls removed, expected:  7, actual:", cell)

    cell = Cell()
    cell.remove_wall(15)
    print("Cell - All walls removed,  expected:  0, actual:", cell)

    print("\n==== Remove multiple Wall Test =====")
    cell = Cell()
    cell.remove_wall(Wall.SOUTH)
    cell.remove_wall(Wall.WEST)
    print("Cell - South and West walls removed, expected:  0011, actual:",
          cell)

    cell = Cell()
    cell.remove_wall(Wall.EAST)
    cell.remove_wall(Wall.WEST)
    print("Cell - East and West walls removed,  expected:  0101, actual:",
          cell)

    cell = Cell()
    cell.remove_wall(Wall.NORTH)
    cell.remove_wall(Wall.EAST)
    print("Cell - South and West walls removed, expected:  1100, actual:",
          cell)

    print("\n==== Visited Wall Test =====")
    cell = Cell()
    print("Cell - Not visited, actual:", cell)
    cell.visit(True)
    print("Cell - Visited, actual:", cell)