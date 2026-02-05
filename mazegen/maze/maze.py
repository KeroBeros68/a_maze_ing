from mazegen.utils.utils import Wall
from mazegen.cell.cell import Cell


class Maze():
    def __init__(self, width: int, height: int):
        self.maze_grid: list[list[Wall]] = []
        self.__width: int = width
        self.__height: int = height

    def init_grid(self):
        self.maze_grid = [[Cell(x, y) for x in range(self.__width)]
                          for y in range(self.__height)]

    def __str__(self) -> str:
        result = []
        for row in self.maze_grid:
            row_str = " ".join(f"{cell._Cell__wall:X}" for cell in row)
            result.append(row_str)
        return "\n".join(result)


if __name__ == "__main__":
    maze = Maze(10, 10)
    maze.init_grid()
    print(maze)
    maze.maze_grid[1][0].remove_wall(Wall.EAST)
    print(maze.maze_grid[1][0])
    print(maze)
