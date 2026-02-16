from mazegen.cell.cell import Cell
from mazegen.maze.maze import Maze
from view.tty.TtyUtils import Canvas, CanvasCell
from view.tty.TtyConsts import Colors, Banners, Panels, Elements, FortyTwoBrick
from model import ConfigModel
from ..View import View
from typing import List, Iterable, Tuple, Optional, Callable
import sys


class TtyView(View):

    def __init__(self, config: ConfigModel) -> None:
        self.__config = config
        sys.stdout.write("\33[H\33[?25l\33[1m\n")
        self.frame_count = 0
        self.exit_found = 0
        self.speed = 15
        self.left_panel_end = 0
        self.right_panel_start = 0
        self.color_theme = 1
        self.color_theme_name = "Cave"
        self.__width = 0
        self.__height = 0
        self.__entry = [0, 0]
        self.__exit = [0, 0]
        self.__seed = None
        self.__view = 3
        self.__perfect = True
        self.__maze = None
        self.xoffset = 0
        self.yoffset = 0
        self.xdim = 0
        self.ydim = 0
        self.grid = None
        self.digger_xy = None
        self.paused = 0
        self.previously_done = 0

    def init_values(self, maze: Maze, speed: int) -> None:
        self.__width = maze.width
        self.__height = maze.height
        self.__entry = maze.entry
        self.__exit = maze.exit
        self.__seed = self.__config.SEED
        if self.__config.DISPLAY_MODE == "tty":
            if self.__config.MODE_GEN == "animated":
                self.__view = 3
            elif self.__config.MODE_GEN == "normal":
                self.__view = 2
        self.__perfect = self.__config.PERFECT
        self.__maze = maze
        self.exit_found = 0
        self.xoffset = 2
        self.xdim = (self.__width * 6) + 3
        xl, yl = Canvas.measure_block(Canvas, Banners.LEFT_BANNER)
        xc, yc = Canvas.measure_block(Canvas, Banners.CENTER_BANNER)
        xr, yr = Canvas.measure_block(Canvas, Banners.RIGHT_BANNER)
        if self.xdim < xl + xc + xr + 6:
            self.xoffset = max(0, int((xl + xc + xr + 6 - self.xdim) / 2 + 2))
            self.xdim = xl + xc + xr + 6
        self.ydim = (self.__height * 3) + 16
        self.yoffset = 10
        self.grid = Canvas(self.xdim, self.ydim, self.color_theme)

    def show_digger(self, digger_xy: Tuple[int, int]) -> None:
        if digger_xy == self.__exit:
            self.exit_found = 1
        x, y = digger_xy
        self.grid.add_block(x * 6 + self.xoffset + 1,
                            y * 3 + self.yoffset + 1, "🔦🤠", Colors.PURPLE)
        cell = f"{self.__maze.maze_grid[y][x].view_cell()}"
        code = int(cell, 16)
        ansi_dim = self.grid.color_wall_ground(1)
        ansi_lit = self.grid.color_wall_ground(2)
        if not code & 1:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell(x * 6 + self.xoffset + lx,
                                         (y - 1) * 3 + self.yoffset + ly,
                                         ansi_dim)
        if not code & 2:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell((x + 1) * 6 + self.xoffset + lx,
                                         y * 3 + self.yoffset + ly, ansi_dim)
        if not code & 4:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell(x * 6 + self.xoffset + lx,
                                         (y + 1) * 3 + self.yoffset + ly,
                                         ansi_dim)
        if not code & 8:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell((x - 1) * 6 + self.xoffset + lx,
                                         y * 3 + self.yoffset + ly,
                                         ansi_dim)
        for ly in range(3):
            for lx in range(6):
                self.grid.color_canvas_cell(x * 6 + self.xoffset + lx,
                                     y * 3 + self.yoffset + ly,
                                     ansi_lit)

    def place_lowblocks_anim(self) -> None:
        x, _ = self.grid.center_block(" Generation steps ",
                                      x_start=1, x_end=self.xdim)
        self.left_panel_end = x
        self.grid.add_block(x - 1, self.ydim - 6,
                            "╤══════════════════╤", Colors.BROWN)
        for by in range(4):
            self.grid.add_block(x - 1, self.ydim - by - 2,
                                "│                  │", Colors.BROWN)
        self.grid.add_block(x - 1, self.ydim - 1,
                            "╧══════════════════╧", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 5,
                            " Generation steps ", Colors.WHITE)
        
        x = self.left_panel_end - 30
        self.grid.add_block(x, self.ydim - 6,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(4):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 5, Panels.ANIM_LEFT_PANEL, Colors.WHITE)
        if self.paused:
            self.grid.add_block(self.left_panel_end - 10,
                                self.ydim - 5, "[ACTIVE]", Colors.GREEN)
        self.grid.add_block(self.left_panel_end - 5, self.ydim - 4,
                            f"{self.speed:03d}", Colors.CYAN)
        dx = self.left_panel_end - 2 - len(self.color_theme_name)
        self.grid.add_block(dx, self.ydim - 3,
                            self.color_theme_name, Colors.CYAN)
        if self.exit_found == 0:
            self.grid.add_block(self.left_panel_end - 4,
                                self.ydim - 2, "🪨", Colors.EXIT)
        elif self.digger_xy is not None:
            self.grid.add_block(self.left_panel_end - 4,
                                self.ydim - 2, "👑", Colors.EXIT)
        frame_counter = self.grid.large_counter_block(self.frame_count)
        x, y = self.grid.center_block(f"{frame_counter}",
                                      x_start=1, x_end=self.xdim)
        self.grid.add_block(x, self.ydim - 4, f"{frame_counter}", Colors.CYAN)

    def place_lowblocks_noanim(self) -> None:
        x = self.left_panel_end - 30
        self.grid.add_block(x, self.ydim - 6,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(4):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 5, Panels.LEFT_PANEL, Colors.WHITE)
        dx = self.left_panel_end - 2 - len(self.color_theme_name)
        self.grid.add_block(dx, self.ydim - 3,
                            self.color_theme_name, Colors.CYAN)

    def place_lowblocks_common(self) -> None:
        if self.__view == 2:
            self.right_panel_start = self.left_panel_end
        else:
            self.right_panel_start = self.left_panel_end + 18
        x = self.right_panel_start
        self.grid.add_block(x, self.ydim - 6,
                            "╤════════════════════════════╤", Colors.BROWN)
        for by in range(4):
            self.grid.add_block(x, self.ydim - by - 2,
                                "│                            │", Colors.BROWN)
        self.grid.add_block(x, self.ydim - 1,
                            "╧════════════════════════════╧", Colors.BROWN)
        self.grid.add_block(x + 1, self.ydim - 5, Panels.RIGHT_PANEL, Colors.WHITE)
        if self.exit_found == 1:
            self.grid.add_block(x + 2, self.ydim - 3, "🪨", Colors.EXIT)
        txt = (f"{self.__width} x {self.__height} "
               f"({self.__width * self.__height})")
        if len(txt) > 13:
            txt = (f"{self.__width}x{self.__height}"
                   f"({self.__width * self.__height})")
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 5, txt, Colors.CYAN)
        ex, ey = self.__entry
        txt = f"{ex}, {ey}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 4, txt, Colors.CYAN)
        ex, ey = self.__exit
        txt = f"{ex}, {ey}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 3, txt, Colors.CYAN)
        txt = f"{self.__perfect}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 2, txt, Colors.CYAN)

    def place_lower_blocks(self) -> None:
        x, y = self.grid.center_block("", x_start=1, x_end=self.xdim)
        self.left_panel_end = x
        self.grid.deco_zone(2, self.ydim - 5, self.xdim - 2, self.ydim - 2,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)

        if self.__view == 3:
            self.place_lowblocks_anim()
        if self.__view == 2 or self.digger_xy is None:
            self.place_lowblocks_noanim()
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
                elif self.__maze.done_gen is True:
                    self.grid.add_maze_locked_cell(dx, dy, lock_code)
                else:
                    self.grid.add_maze_cell(dx, dy, "F")
        x, y = self.__entry
        self.grid.add_block(x * 6 + self.xoffset + 2,
                            y * 3 + self.yoffset + 1,
                            "🚪", Colors.ENTRY)
        x, y = self.__exit
        if self.exit_found == 0:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "👑", Colors.EXIT)
        else:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "🪨", Colors.EXIT)

    def render_digger(self, maze: Maze) -> None:
        if self.__maze.done_gen == False:
            self.digger_xy = self.__maze.active_cell
        else:
            self.previously_done = 1
            self.digger_xy = None
        if self.digger_xy is not None:
            self.show_digger(self.digger_xy)
        elif self.__view == 3:
            x, y = self.grid.center_block("👑🤠👍", x_start=1, x_end=self.xdim)
            self.grid.add_block(x - 2, 7, "👑🤠👍", "")

    def render(self, maze: Maze, speed: int, count_as_step: Optional[int] = 1) -> None:
        if maze.restart is True:
            self.previously_done = 0
            self.frame_count = 0
            maze.restart = False
        if self.previously_done == 1 and self.__maze.done_gen == False:
            self.previously_done = 0
            self.frame_count = 0
        if self.frame_count == 0:
            self.init_values(maze, speed)
        self.speed = speed
        self.frame_count += count_as_step
        self.color_theme_name = self.grid.color_theme_name
        self.grid.clear_canvas(" ", "")
        self.grid.template()
        self.render_maze(maze)
        self.render_digger(maze)
        self.place_lower_blocks()
        self.grid.print_canvas()

    def change_color(self, new_color: int) -> None:
        self.color_theme += new_color
        if self.color_theme < 1:
            self.color_theme = 5
        if self.color_theme > 5:
            self.color_theme = 1
        self.grid.color_theme = self.color_theme
        self.grid.color_wall_ground(0)
