from mazegen.maze.maze import Maze
from ..View import View


class BasicView(View):
    def __init__(self) -> None:
        super().__init__()

    def render(self, maze: Maze, speed: int) -> None:
        print("\33[H")
        print("\n Mon maze, speed:", speed, maze.active_cell)
        print(maze)
        print("\n Generation finished:", maze.done_gen)

    def change_color(self, new_color: int) -> None:
        print("coucou")
