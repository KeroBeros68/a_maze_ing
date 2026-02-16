"""Basic text-based maze visualization.

This module provides a simple terminal-based maze visualization that displays
the maze grid in ASCII art format with walls represented graphically.

Classes:
    BasicView: Text-based maze renderer
"""

from typing import List, Optional
from mazegen.cell.cell import Cell
from mazegen.maze.maze import Maze
from view.utils.Colors import ColorsTty
from ..View import View


class BasicView(View):
    """Simple text-based maze visualization using ASCII art.

    Renders the maze grid in the terminal with cells represented as boxes
    with visible walls. Shows generation progress and current active cell.
    """

    def __init__(self) -> None:
        """Initialize the BasicView."""
        self.__color_list: Optional[List[ColorsTty]] = (
            ColorsTty.get_ordered_colors()
        )
        self.__active_color: Optional[ColorsTty] = self.__color_list[0]
        self.__entry_color: Optional[ColorsTty] = ColorsTty.ENTRY
        self.__exit_color: Optional[ColorsTty] = ColorsTty.EXIT
        self.__closed_color: Optional[ColorsTty] = ColorsTty.CLOSED

    def render(self, maze: Maze, speed: int) -> None:
        """Render the maze to terminal output.

        Displays the maze grid, current speed, active cell position,
        and generation status.

        Args:
            maze: The Maze object to render
            speed: Current animation speed in FPS
        """
        print("\n\n\n\33[HMon maze, speed:",
              speed, maze.active_cell)
        print("\n\n\n")
        print(
            self.print_maze(maze),
            ColorsTty.RESET.value,
        )
        print(f"\n Generation finished: {maze.done_gen} ")

    def change_color(self, new_color: int) -> None:
        """Change the display color based on direction.

        Args:
            new_color: -1 to go to previous color, 1 to go to next color
        """
        if self.__color_list is None or len(self.__color_list) == 0:
            return

        # Find current active color index
        current_index = self.__color_list.index(self.__active_color)

        if new_color == -1:  # Previous color
            new_index = (current_index - 1) % len(self.__color_list)
        elif new_color == 1:  # Next color
            new_index = (current_index + 1) % len(self.__color_list)
        else:
            return

        self.__active_color = self.__color_list[new_index]

    def view_cell(self, cell: Cell) -> str:
        """Generate ASCII art representation of a single cell.

        Args:
            cell: The Cell object to visualize

        Returns:
            str: Multi-line ASCII art string representing the cell with walls
        """
        wall = f"{self.__active_color.value}▒▒"

        if cell.is_entry:
            center_cell = f"{ColorsTty.ENTRY.value}░░"
        elif cell.is_exit:
            center_cell = f"{ColorsTty.EXIT.value}░░"
        elif cell.visited:
            center_cell = f"{ColorsTty.WHITE.value}░░"
        else:
            center_cell = f"{self.__closed_color.value}░░"

        if cell.visited:
            path = f"{ColorsTty.WHITE.value}░░"
        else:
            path = f"{self.__closed_color.value}░░"

        return "\n".join(
            [
                f"{wall}{wall if cell.wall & 0b0001 else path}{wall}",
                f"{wall if cell.wall & 0b1000 else path}"
                f"{center_cell}"
                f"{wall if cell.wall & 0b0010 else path}",
                f"{wall}{wall if cell.wall & 0b0100 else path}{wall}",
            ]
        )

    def print_maze(self, maze: Maze) -> str:
        """Generate ASCII art representation of the entire maze.

        Args:
            maze: The Maze object to visualize

        Returns:
            str: Multi-line ASCII art string representing the entire maze grid
        """
        result = ""
        for row in maze.maze_grid:
            row_str = ["            ", "            ", "            "]
            for x, cell in enumerate(row):
                cell_view = self.view_cell(cell).splitlines()
                for i in range(3):
                    row_str[i] += cell_view[i]
            result += "\n".join(row_str) + "\n"
        return result
