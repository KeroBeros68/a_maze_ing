from mazegen.cell.cell import Cell
from mazegen.maze.maze import Maze
from ..View import View


class BasicView(View):
    def __init__(self) -> None:
        super().__init__()

    def render(self, maze: Maze, speed: int) -> None:
        print("\33[H")
        print("\n Mon maze, speed:", speed, maze.active_cell)
        print(self.print_maze(maze))
        print()
        print(maze)
        print("\n Generation finished:", maze.done_gen)

    def change_color(self, new_color: int) -> None:
        print("coucou")

    def view_cell(self, cell: Cell) -> str:
        return "\n".join(
            [
                f"/ {'==' if cell.wall & 0b0001 else '  '} \\",
                f"{'| ' if cell.wall & 0b1000 else '  '}  "
                f"{' |' if cell.wall & 0b0010 else '  '}",
                f"\\ {'==' if cell.wall & 0b0100 else '  '} /",
            ]
        )

    def print_maze(self, maze: Maze) -> str:
        result = ""
        for row in maze.maze_grid:
            row_str = ["", "", ""]
            for x, cell in enumerate(row):
                cell_view = self.view_cell(cell).splitlines()
                for i in range(3):
                    row_str[i] += cell_view[i]
            result += "\n".join(row_str) + "\n"
        return result
