from mazegen.maze.maze import Maze
from .View import View


class BasicView(View):
    def __init__(self):
        super().__init__()

    def render(self, maze: Maze, speed) -> None:
        print("\n Mon maze, speed:", speed)
        print(maze)
