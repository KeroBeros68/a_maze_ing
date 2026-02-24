"""Interactive game mode for maze traversal.

This module implements interactive gameplay where users navigate a character
through the generated maze to reach the exit point.

Classes:
    Game: Handles maze game mechanics and player movement
"""

from view.tty.TtyConsts import Endgame, Elements, Colors
from view.tty.TtyUtils import Canvas
from view.tty.TtyView import TtyView
from view.tty.TtyLight import Light
from mazegen.maze.maze import Maze
from typing import Tuple, Optional
import time

Event = Tuple[str, object | None]


class Game:
    """Interactive maze game with player movement and lighting.

    Allows users to navigate through the maze using keyboard controls,
    with dynamic lighting effects and collision detection.
    """

    def __init__(self, view: TtyView, grid: Canvas, light: Light,
                 maze: Maze) -> None:
        """Initialize the game with maze and rendering components.

        Args:
            view: TtyView instance
            grid: Canvas for rendering
            light: Light effects handler
            maze: The Maze object to play in
            events: Optional event queue for keyboard input
        """
        self.view = view
        self.grid = grid
        self.light = light
        self.__maze = maze
        self.x1 = self.view.xoffset
        self.y1 = self.view.yoffset
        self.x2 = self.__maze.width * 6 + self.x1
        self.y2 = self.__maze.height * 3 + self.y1
        self.x_cell_pc, self.y_cell_pc = self.__maze.entry
        self.x_cell_in, self.y_cell_in = self.__maze.entry
        self.x_cell_out, self.y_cell_out = self.__maze.exit

    def move(self, key: str | None = None) -> None:
        self.x_pc = self.x_cell_pc * 6 + self.view.xoffset + 2
        self.y_pc = self.y_cell_pc * 3 + self.view.yoffset + 1
        self.x_in = self.x_cell_in * 6 + self.view.xoffset + 2
        self.y_in = self.y_cell_in * 3 + self.view.yoffset + 1
        self.x_out = self.x_cell_out * 6 + self.view.xoffset + 2
        self.y_out = self.y_cell_out * 3 + self.view.yoffset + 1

        self.grid.add_block(self.x_in, self.y_in, "🚪")
        self.light.light_cell_from_xy(x=self.x_in, y=self.y_in, lit=1.0)
        self.grid.add_block(self.x_out, self.y_out, "👑")
        self.light.light_cell_from_xy(x=self.x_out, y=self.y_out, lit=1.0)
        self.grid.add_block(self.x_pc, self.y_pc, "🤓")
        self.light.light_cell_from_xy(x=self.x_pc, y=self.y_pc, lit=3.0)
        self.grid.print_canvas()

        if key is None:
            if self.x_pc == self.x_out and self.y_pc == self.y_out:
                self.endgame()
            return
        x, y = self.x_cell_pc, self.y_cell_pc
        cell_code = int(self.__maze.maze_grid[y][x].view_cell(), 16)
        go_x, go_y = 0, 0
        if key in ("Z", "W") and not cell_code & 1:
            self.y_cell_pc -= 1
            go_y = -1
        elif key in ("S") and not cell_code & 4:
            self.y_cell_pc += 1
            go_y = 1
        elif key in ("D") and not cell_code & 2:
            self.x_cell_pc += 1
            go_x = 2
        elif key in ("Q", "A") and not cell_code & 8:
            self.x_cell_pc -= 1
            go_x = -2
        else:
            if self.x_pc == self.x_out and self.y_pc == self.y_out:
                self.endgame()
            return

        self.view.game_moves += 1
        self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)
        for _ in range(3):
            if ((self.x_pc != self.x_in or self.y_pc != self.y_in)
               and (self.x_pc != self.x_out or self.y_pc != self.y_out)):
                self.grid.add_block(self.x_pc, self.y_pc, "  ")
                self.light.light_cell_from_xy(x=self.x_pc, y=self.y_pc,
                                              lit=1.0)
            self.x_pc += go_x
            self.y_pc += go_y
            self.grid.add_block(self.x_pc, self.y_pc, "🤓")
            self.light.light_cell_from_xy(x=self.x_pc, y=self.y_pc,
                                          lit=3.0)
            if self.x_pc != self.x_in or self.y_pc != self.y_in:
                self.grid.add_block(self.x_in, self.y_in, "🚪")
                self.light.light_cell_from_xy(x=self.x_in, y=self.y_in,
                                              lit=1.0)
            if self.x_pc != self.x_out or self.y_pc != self.y_out:
                self.grid.add_block(self.x_out, self.y_out, "👑")
                self.light.light_cell_from_xy(x=self.x_out, y=self.y_out,
                                              lit=1.0)
            self.grid.print_canvas()
            time.sleep(1 / self.view.speed)
            if self.x_pc == self.x_out and self.y_pc == self.y_out:
                self.endgame()

    def endgame(self) -> None:
        panel_x, panel_y = self.grid.center_block(
            Endgame.FRAME,
            x_start=self.x1, x_end=self.x2,
            y_start=self.y1, y_end=self.y2
            )
        panel_x_dim, panel_y_dim = self.grid.measure_block(Endgame.FRAME)
        panel_x_end = panel_x + panel_x_dim - 1
        panel_y_end = panel_y + panel_y_dim - 1
        self.grid.deco_zone(panel_x, panel_y,
                            panel_x_end, panel_y_end,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)
        self.grid.add_block(panel_x, panel_y, Endgame.FRAME,
                            Colors.BROWN, transparent=True)
        self.grid.add_block(panel_x + 1, panel_y + 1, Endgame.TEXT,
                            Colors.WHITE, transparent=True)
        r, g, b, _, _, _ = self.grid.color_wall_ground_raw(1)
        r = min(255, r * 2)
        g = min(255, g * 2)
        b = min(255, b * 2)
        ansi_theme = f"\33[38;2;{r};{g};{b}m\33[48;2;0;0;0m"
        self.grid.add_block(panel_x + 1, panel_y + 4, Endgame.BUTTONS,
                            ansi_theme, transparent=True)
        txt = str(self.view.game_moves)
        self.grid.add_block(panel_x_end - 2 - len(txt), panel_y + 1, txt,
                            ansi_theme, transparent=True)
        txt = str(len(self.__maze.shortest_path))
        self.grid.add_block(panel_x_end - 2 - len(txt), panel_y + 2, txt,
                            ansi_theme, transparent=True)
        efficiency = (100 * len(self.__maze.shortest_path)
                      / self.view.game_moves)
        txt = f"{efficiency:2.2f} %"
        self.grid.add_block(panel_x_end - 2 - len(txt), panel_y + 3, txt,
                            ansi_theme, transparent=True)
        if efficiency == 100:
            self.grid.add_block(panel_x + 1, panel_y + 1, Endgame.AMAZING,
                                ansi_theme, transparent=True)
        elif efficiency >= 75:
            self.grid.add_block(panel_x + 1, panel_y + 1, Endgame.WELL_DONE,
                                ansi_theme, transparent=True)
        elif efficiency >= 50:
            self.grid.add_block(panel_x + 1, panel_y + 1, Endgame.NOT_BAD,
                                ansi_theme, transparent=True)
        else:
            self.grid.add_block(panel_x + 1, panel_y + 1, Endgame.LOST,
                                ansi_theme, transparent=True)

        self.grid.print_canvas()
