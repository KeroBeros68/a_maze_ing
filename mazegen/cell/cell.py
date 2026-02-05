from ..utils import Wall


class Cell():
    def __init__(self):
        self.__wall: int = 0xF
        self.__visited: bool = False

    def remove_wall(self, wall: Wall):
        self.__wall &= ~wall

    def visit(self, is_visited: bool):
        self.__visited = is_visited

    def __str__(self):
        return f"{self.__wall}"


cell = Cell()
cell.remove_wall(Wall.EAST)
print(cell)