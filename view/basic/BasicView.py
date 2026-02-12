from mazegen.maze.maze import Maze
from ..View import View


class BasicView(View):
    def __init__(self) -> None:
        super().__init__()

    def render(self, maze: Maze, speed: int) -> None:
        print("\33[H")
        print("\n Mon maze, speed:", speed)
        print(maze)

    def change_color(self, new_color: int) -> None:
        print("coucou")
