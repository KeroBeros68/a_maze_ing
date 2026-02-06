from mazegen.algorithms.backtracking import backtrack
from mazegen.maze.maze import Maze
from model import ConfigModel


class MazeGenerator():
    def __init__(self, config: ConfigModel):
        self.__width = config.WIDTH
        self.__height = config.HEIGHT
        self.__entry = config.ENTRY
        self.__exit = config.EXIT
        self.maze: Maze = None

    def generate_maze(self) -> Maze:
        self.maze = Maze(self.__width, self.__height, self.__entry,
                         self.__exit)
        self.maze.init_grid()
        # algo de generation
        x, y = self.__entry
        self.maze = backtrack(self.maze, x, y)
        return self.maze
