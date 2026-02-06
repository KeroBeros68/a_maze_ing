from mazegen.utils.utils import Wall


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.__wall: int = 0xF
        self.visited: bool = False
        self.__x: int = x
        self.__y: int = y

    def remove_wall(self, wall: Wall) -> None:
        self.__wall &= ~wall

    def visit(self, is_visited: bool) -> None:
        self.visited = is_visited

    def __str__(self) -> str:
        return (
            f"Cellule: {self.__wall:2}  {self.__wall:04b}  {self.__wall:X}"
            f" is visited: {self.visited} "
            f"position in maze: {self.__x}, {self.__y}"
        )

    def view_cell(self) -> str:
        wall_hex = f"{self.__wall:X}"

        return f"{wall_hex}"
    # def view_cell(self) -> str:
    #     return [
    #         f"/ {'==' if self.__wall & 0b0001 else '  '} \\",
    #         f"{'| ' if self.__wall & 0b1000 else "  "}  {' |' if self.__wall
    # & 0b0010 else "  "}",
    #         f"\\ {'==' if self.__wall & 0b0100 else '  '} /",
    #     ]


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
