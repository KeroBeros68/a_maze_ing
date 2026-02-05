from mazegen.maze.maze import Maze


class MazeGenerator():
    def __init__(self, config):
        self.__width = config.WIDTH
        self.__height = config.HEIGHT
        self.maze = []

    def generate_maze(self) -> Maze:
        self.maze = Maze(self.__width, self.__height)
        # algo de generation
        return self.maze
