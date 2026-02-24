"""TTY (teletypewriter) maze visualization with advanced rendering.

This module provides an advanced terminal-based maze visualization using
ANSI escape codes with multiple display modes, animations, lighting effects,
and interactive gameplay.

Classes:
    TtyView: Advanced TTY-based maze visualization
"""

from mazegen.maze.maze import Maze
from view.tty.TtyConsts import Colors, Banners, Panels, Elements
from mazegen.model import ConfigModel
from ..View import View
from typing import Tuple, Optional, Iterable
import sys
import time


class TtyView(View):
    """Advanced TTY-based maze visualization with rendering effects.

    Provides animated maze generation display, lighting effects, and
    interactive game mode with keyboard controls. Manages canvas rendering,
    animations, and UI elements.
    """

    def __init__(self, config: ConfigModel) -> None:
        """Initialize the TTY view with configuration settings."""
        self.__config = config
        sys.stdout.write("\33[H\33[?25l\33[1m\n")
        self.frame_count = 0
        self.game_moves = 0
        self.exit_found = 0
        self.speed = 15
        self.left_panel_end = 0
        self.right_panel_start = 0
        self.color_theme = 1
        self.color_theme_name = "Cave"
        self.__width = 0
        self.__height = 0
        self.__entry = 0, 0
        self.__exit = 0, 0
        self.__seed: str | None = None
        self.__view = 3
        self.__perfect = True
        self.__algo = ""
        self.xoffset = 0
        self.yoffset = 0
        self.xdim = 0
        self.ydim = 0
        self.digger_xy: Tuple[int, int] | None = None
        self.paused = False
        self.previously_done = 0
        self.gen_step = 0
        self.ansi_theme = Colors.CYAN

    def init_values(self, maze: Maze, speed: int, algo: str,
                    seed: Optional[str] = "") -> None:
        """Initialize values for maze rendering and display.

        Sets up the canvas, grid, lighting, animations, and game components
        based on the maze configuration and display mode.

        Args:
            maze: The Maze object to render
            speed: Animation speed in frames per second
            algo: Maze generation algorithm name
            seed: Random seed used for maze generation
        """
        self.__width = maze.width
        self.__height = maze.height
        self.__entry = maze.entry
        self.__exit = maze.exit
        self.__seed = seed
        self.exit_found = 0
        if self.__config.DISPLAY_MODE == "tty":
            if self.__config.MODE_GEN == "animated":
                self.__view = 3
            elif self.__config.MODE_GEN == "static":
                self.__view = 2
                self.exit_found = 1
        self.view = self.__view
        self.__maze = maze
        self.__perfect = self.__maze.perfect
        self.__algo = algo
        self.xdim = (self.__width * 6) + 3
        self.xoffset = 2
        self.ydim = (self.__height * 3) + 18
        xl, _ = self.measure_block(Banners.LEFT_BANNER)
        xc, _ = self.measure_block(Banners.CENTER_BANNER)
        xr, _ = self.measure_block(Banners.RIGHT_BANNER)
        if self.xdim < xl + xc + xr + 6:
            self.xoffset = max(0, int((xl + xc + xr + 6 - self.xdim) / 2 + 2))
            self.xdim = xl + xc + xr + 6
        self.yoffset = 10
        from view.tty.TtyUtils import Canvas
        self.grid = Canvas(self, self.xdim, self.ydim, self.color_theme,
                           self.__maze)
        from view.tty.TtyLight import Light
        self.light = Light(self, self.grid, self.__maze)
        from view.tty.TtyAnims import Anims
        self.anim = Anims(self, self.grid, self.light,
                          self.__maze, self.__view)
        from view.tty.TtyGame import Game
        self.game = Game(self, self.grid, self.light, self.__maze)
        r, g, b, _, _, _ = self.grid.color_wall_ground_raw(1)
        r = min(255, r * 2)
        g = min(255, g * 2)
        b = min(255, b * 2)
        self.ansi_theme = f"\33[38;2;{r};{g};{b}m\33[48;2;0;0;0m"

    def measure_block(self, block: str | Iterable[str]) -> tuple[int, int]:
        """Measure the dimensions of a text block.

        Args:
            block: String or iterable of strings to measure

        Returns:
            Tuple[int, int]: (width, height) of the block
        """
        if isinstance(block, str):
            lines = block.splitlines()
        else:
            lines = list(block)
        if not lines:
            return (0, 0)
        width = max(len(line) for line in lines)
        height = len(lines)
        return (width, height)

    def place_lowblocks_anim(self) -> None:
        x, _ = self.grid.center_block("  Generation steps  ",
                                      x_start=1, x_end=self.xdim)
        self.left_panel_end = x
        self.grid.add_block(x - 1, self.ydim - 8,
                            "╤════════════════════╤", Colors.BROWN)
        for by in range(6):
            self.grid.add_block(x - 1, self.ydim - by - 2,
                                "│                    │", Colors.BROWN)
        self.grid.add_block(x - 1, self.ydim - 1,
                            "╧════════════════════╧", Colors.BROWN)
        self.grid.deco_zone(x, self.ydim - 7, x + 19, self.ydim - 2,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)
        self.grid.add_block(x, self.ydim - 7,
                            "  Generation steps  ", Colors.WHITE,
                            transparent=True)

        x = self.left_panel_end - 30
        self.grid.add_block(x, self.ydim - 8,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(6):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 7, Panels.ANIM_LEFT_PANEL,
                            Colors.WHITE)
        if self.paused:
            self.grid.add_block(self.left_panel_end - 10,
                                self.ydim - 7, "[ACTIVE]", Colors.GREEN)
        self.grid.add_block(self.left_panel_end - 5, self.ydim - 6,
                            f"{self.speed:03d}", self.ansi_theme)
        dx = self.left_panel_end - 2 - len(self.color_theme_name)
        self.grid.add_block(dx, self.ydim - 5,
                            self.color_theme_name, self.ansi_theme)
        if self.exit_found == 0:
            self.grid.add_block(self.left_panel_end - 4,
                                self.ydim - 2, "  ", Colors.EXIT)
        elif self.digger_xy is not None:
            self.grid.add_block(self.left_panel_end - 4,
                                self.ydim - 2, "  ", Colors.EXIT)
        frame_counter = self.grid.large_counter_block(self.frame_count)
        x, y = self.grid.center_block(f"{frame_counter}",
                                      x_start=1, x_end=self.xdim)
        self.grid.add_block(x, self.ydim - 5, f"{frame_counter}",
                            self.ansi_theme, transparent=True)

    def place_lowblocks_noanim(self) -> None:
        x = self.left_panel_end - 30
        self.grid.add_block(x, self.ydim - 8,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(6):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 7,
                            Panels.LEFT_PANEL, Colors.WHITE)
        dx = self.left_panel_end - 2 - len(self.color_theme_name)
        self.grid.add_block(dx, self.ydim - 5,
                            self.color_theme_name, self.ansi_theme)

    def place_lowblocks_game(self) -> None:
        x = self.left_panel_end - 30
        self.grid.add_block(x, self.ydim - 8,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(6):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 7,
                            Panels.GAME_PANEL, Colors.WHITE)
        dx = self.left_panel_end - 2 - len(self.color_theme_name)
        self.grid.add_block(dx, self.ydim - 5,
                            self.color_theme_name, self.ansi_theme)

    def place_lowblocks_common(self) -> None:
        if self.__view == 2:
            self.right_panel_start = self.left_panel_end
        else:
            self.right_panel_start = self.left_panel_end + 20
        x = self.right_panel_start
        self.grid.add_block(x, self.ydim - 8,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(6):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │",
                                Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 7,
                            Panels.RIGHT_PANEL, Colors.WHITE)
        # if self.exit_found == 1 and self.__maze.gen_step != 5:
        if self.exit_found == 1:
            self.grid.add_block(x + 2, self.ydim - 5, "👑", Colors.EXIT)
        # if self.exit_found == 1 and self.__maze.gen_step == 5:
        #     self.grid.add_block(x + 2, self.ydim - 5, "🪨", Colors.EXIT)
        txt = (f"{self.__width} x {self.__height} "
               f"({self.__width * self.__height})")
        if len(txt) > 13:
            txt = (f"{self.__width}x{self.__height}"
                   f"({self.__width * self.__height})")
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 7, txt, self.ansi_theme)
        ex, ey = self.__entry
        txt = f"{ex}, {ey}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 6, txt, self.ansi_theme)
        ex, ey = self.__exit
        txt = f"{ex}, {ey}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 5, txt, self.ansi_theme)
        txt = f"{self.__perfect}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 4, txt, self.ansi_theme)
        txt = f"{self.__seed}"
        if len(txt) <= 16:
            dx = x + 28 - len(txt)
            self.grid.add_block(dx, self.ydim - 3, txt, self.ansi_theme)
        else:
            mid = len(txt) // 2
            txt1 = txt[:mid]
            txt2 = txt[mid:]
            dx1 = x + 28 - len(txt1)
            dx2 = x + 28 - len(txt2)
            self.grid.add_block(dx1, self.ydim - 3, txt1, self.ansi_theme)
            self.grid.add_block(dx2, self.ydim - 2, txt2, self.ansi_theme)

    def place_lower_blocks(self) -> None:
        x, y = self.grid.center_block("", x_start=1, x_end=self.xdim)
        self.left_panel_end = x
        self.grid.deco_zone(2, self.ydim - 7, self.xdim - 2, self.ydim - 2,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)
        if self.__view == 3:
            self.place_lowblocks_anim()
        if self.__view == 2 or 9 > self.__maze.gen_step >= 3:
            self.place_lowblocks_noanim()
        if self.__maze.gen_step == 9:
            self.place_lowblocks_game()
        if self.__view == 2 or self.__view == 3:
            self.place_lowblocks_common()

    def render_maze(self, maze: Maze) -> None:
        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                lock_code = self.__maze.maze_grid[y][x].lock_code
                dx = x * 6 + self.xoffset
                dy = y * 3 + self.yoffset
                if lock_code == " ":
                    cell_view = f"{self.__maze.maze_grid[y][x].view_cell()}"
                    self.grid.add_maze_cell(dx, dy, cell_view)
                elif self.__maze.gen_step >= 3:
                    self.grid.add_maze_locked_cell(dx, dy, lock_code)
                else:
                    self.grid.add_maze_cell(dx, dy, "F")
        x, y = self.__entry
        self.grid.add_block(x * 6 + self.xoffset + 2,
                            y * 3 + self.yoffset + 1,
                            "🚪", Colors.ENTRY)
        self.light.light_cell(x=x, y=y, lit_max=1.0, dim_lit=0.5)
        x, y = self.__exit
        if self.exit_found == 0:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "  ", Colors.EXIT)
        else:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "👑", "")
            self.light.light_cell(x=x, y=y, lit_max=1.0, dim_lit=0.5)

    def render_digger(self, maze: Maze) -> None:
        if self.__maze.gen_step == 1 and self.__maze.active_cell:
            ax, ay, aw = self.__maze.active_cell
            self.digger_xy = ax, ay
        else:
            self.previously_done = 1
            self.digger_xy = None
        if self.digger_xy is not None and self.digger_xy == self.__exit:
            self.exit_found = 1
        if self.digger_xy is not None and self.__algo == "backtracking":
            self.anim.show_digger(self.digger_xy)
        elif self.digger_xy is not None and self.__algo == "prim":
            self.anim.show_firewall(self.digger_xy)

    def show_path(self) -> None:
        path = self.__maze.shortest_path
        xin, yin = self.__maze.entry
        xout, yout = self.__maze.exit
        x, y = xin, yin
        dir_way = "  "
        for i, direction in enumerate(path):
            next_direction = path[i + 1] if i + 1 < len(path) else None
            if direction == "N":
                y -= 1
                if next_direction == "W":
                    dir_way = " ⮢"
                elif next_direction == "N":
                    dir_way = " ⭡"
                elif next_direction == "E":
                    dir_way = " ⮣"
            elif direction == "S":
                y += 1
                if next_direction == "W":
                    dir_way = "⮠ "
                elif next_direction == "S":
                    dir_way = "⭣ "
                elif next_direction == "E":
                    dir_way = "⮡ "
            elif direction == "E":
                x += 1
                if next_direction == "N":
                    dir_way = " ⮥"
                elif next_direction == "E":
                    dir_way = "⭢ "
                elif next_direction == "S":
                    dir_way = "⮧ "
            elif direction == "W":
                x -= 1
                if next_direction == "N":
                    dir_way = " ⮤"
                elif next_direction == "W":
                    dir_way = "⭠ "
                elif next_direction == "S":
                    dir_way = "⮦ "
            if x == xout and y == yout:
                continue
            x_grid = x * 6 + self.xoffset + 2
            y_grid = y * 3 + self.yoffset + 1
            self.grid.add_block(x_grid, y_grid, dir_way)

    def render(self, maze: Maze, speed: int, algo: str,
               seed: Optional[str] = "",
               count_as_step: Optional[int] = 1,
               key: str | None = None) -> None:
        if maze.restart is True:
            self.previously_done = 0
            self.frame_count = 0
            self.game_moves = 0
            maze.restart = False
        if self.previously_done == 1 and self.__maze.gen_step < 3:
            self.previously_done = 0
            self.frame_count = 0
            self.game_moves = 0
        if self.frame_count == 0:
            self.init_values(maze, speed, algo, seed)
        self.speed = speed
        if count_as_step:
            self.frame_count += count_as_step
        self.color_theme_name = self.grid.color_theme_name
        self.grid.clear_canvas(" ", "")
        self.grid.template()
        self.render_maze(maze)
        self.place_lower_blocks()

        if self.__maze.gen_step == 1:
            self.gen_step = 1
            self.render_digger(maze)
        elif self.__maze.gen_step == 2:
            if self.gen_step == 1:
                time.sleep(1)
            self.gen_step = 2
            self.anim.collapse_wall(maze)
        elif self.__maze.gen_step == 4:
            if self.__view == 3:
                self.anim.anim_raider(maze)
            else:
                self.show_path()
                self.__maze.gen_step = 5
        elif self.__maze.gen_step == 5:
            self.render_maze(maze)
            self.show_path()
        elif self.__maze.gen_step == 6:
            self.render_maze(maze)
            self.__maze.gen_step = 3
        elif self.__maze.gen_step == 9:
            self.game.move(key)

        self.place_lower_blocks()
        self.grid.print_canvas()

    def change_color(self, new_color: int) -> None:
        self.color_theme += new_color
        if self.color_theme < 1:
            self.color_theme = 8
        if self.color_theme > 8:
            self.color_theme = 1
        self.grid.color_theme = self.color_theme
        r, g, b, _, _, _ = self.grid.color_wall_ground_raw(1)
        r = min(255, r * 2)
        g = min(255, g * 2)
        b = min(255, b * 2)
        self.ansi_theme = f"\33[38;2;{r};{g};{b}m\33[48;2;0;0;0m"
        self.grid.color_wall_ground(0)
        if self.__maze.gen_step == 9:
            self.game.move(None)
