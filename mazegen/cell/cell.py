from ..utils import Wall, Direction


class Cell():
    def __init__(self):
        self.__wall: int = 0xF
        self.__visited: bool = False

    def remove_wall(self, wall: Wall):
        self.__wall &= ~wall

    def visit(self, is_visited: bool):
        self.__visited = is_visited

    def __str__(self):
        return (f"Cellule: {self.__wall:2}  {self.__wall:04b}  {self.__wall:X}"
                f" is visited: {self.__visited}")


if __name__ == "__main__":
    list_cell = []
    for _ in range(4):
        cell = Cell()
        list_cell.append(cell)

    list_cell[0].remove_wall(Wall.EAST)
    list_cell[1].remove_wall(Direction.EAST.opposite.wall)
    list_cell[1].visit(True)
    list_cell[2].remove_wall(15)
    for c in list_cell:
        print(c)
