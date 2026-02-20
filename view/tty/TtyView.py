from mazegen.maze.maze import Maze
from view.tty.TtyUtils import Canvas
from view.tty.TtyConsts import Colors, Banners, Panels, Elements
from model import ConfigModel
from ..View import View
from typing import Tuple, Optional
import sys
import time


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

    def init_values(self, maze: Maze, speed: int, algo: str,
                    seed: Optional[str] = "") -> None:
        self.__width = maze.width
        self.__height = maze.height
        self.__entry = maze.entry
        self.__exit = maze.exit
        self.__seed = seed
        self.exit_found = 0
        if self.__config.DISPLAY_MODE == "tty":
            if self.__config.MODE_GEN == "animated":
                self.__view = 3
            elif self.__config.MODE_GEN == "normal":
                self.__view = 2
                self.exit_found = 1
        self.__maze = maze
        self.__perfect = self.__maze.perfect
        self.__algo = algo
        self.xoffset = 2
        self.xdim = (self.__width * 6) + 3
        self.ydim = (self.__height * 3) + 18
        self.grid = Canvas(self.xdim, self.ydim, self.color_theme)
        xl, yl = self.grid.measure_block(Banners.LEFT_BANNER)
        xc, yc = self.grid.measure_block(Banners.CENTER_BANNER)
        xr, yr = self.grid.measure_block(Banners.RIGHT_BANNER)
        if self.xdim < xl + xc + xr + 6:
            self.xoffset = max(0, int((xl + xc + xr + 6 - self.xdim) / 2 + 2))
            self.xdim = xl + xc + xr + 6
            self.grid.width = self.xdim
        self.yoffset = 10

    def show_digger(self, digger_xy: Tuple[int, int]) -> None:
        x, y = digger_xy
        self.grid.add_block(x * 6 + self.xoffset + 1,
                            y * 3 + self.yoffset + 1, "🔨🧔", Colors.PURPLE)
        cell = f"{self.__maze.maze_grid[y][x].view_cell()}"
        code = int(cell, 16)
        ansi_dim = self.grid.color_wall_ground(1)
        ansi_lit = self.grid.color_wall_ground(2)

        def light_zone(xbase: int, ybase: int, ansi: str) -> None:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell(xbase + lx, ybase + ly, ansi)

        if not code & 1:
            light_zone(x * 6 + self.xoffset,
                       (y - 1) * 3 + self.yoffset, ansi_dim)
        if not code & 2:
            light_zone((x + 1) * 6 + self.xoffset,
                       y * 3 + self.yoffset, ansi_dim)
        if not code & 4:
            light_zone(x * 6 + self.xoffset,
                       (y + 1) * 3 + self.yoffset, ansi_dim)
        if not code & 8:
            light_zone((x - 1) * 6 + self.xoffset,
                       y * 3 + self.yoffset, ansi_dim)
        light_zone(x * 6 + self.xoffset,
                   y * 3 + self.yoffset, ansi_lit)

    def show_firewall_propagation(self) -> tuple[int, int]:
        ansi_off = self.grid.color_wall_ground(0)
        ansi_dim = self.grid.color_wall_ground(1)
        ansi_lit = self.grid.color_wall_ground(2)
        ansi_bright = self.grid.color_wall_ground(4)
        on_fire = 0
        cell_done = 0

        def ignite(cx: int, cy: int, code: int, center: str,
                   sides: str, ansi: str) -> None:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell(cx + lx - 1, cy + ly - 1, ansi)
            self.grid.add_block(cx, cy, f"{center}", ansi)
            if not code & 1:
                self.grid.add_block(cx, cy - 1, f"{sides}{sides}", ansi)
            if not code & 4:
                self.grid.add_block(cx, cy + 1, f"{sides}{sides}", ansi)
            if not code & 2:
                self.grid.add_block(cx + 4, cy, f"{sides}", ansi)
            if not code & 8:
                self.grid.add_block(cx - 2, cy, f"{sides}", ansi)

        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                since = self.__maze.maze_grid[y][x].visited_since
                if since > 0:
                    self.__maze.maze_grid[y][x].visited_since = since + 1
                if 0 < since <= 50:
                    on_fire += 1
                cx = x * 6 + self.xoffset + 1
                cy = y * 3 + self.yoffset + 1
                if (self.__maze.maze_grid[y][x].visited is True
                   or self.__maze.maze_grid[y][x].locked is True):
                    cell_done += 1
                cell = f"{self.__maze.maze_grid[y][x].view_cell()}"
                code = int(cell, 16)
                since = self.__maze.maze_grid[y][x].visited_since
                if 0 < since <= 5:
                    ignite(cx, cy, code, " 💥 ", "🔥", ansi_bright)
                elif 5 < since <= 20:
                    ignite(cx, cy, code, "🔥🔥", "🔥", ansi_lit)
                elif 20 < since <= 30:
                    ignite(cx, cy, code, " 🔥 ", "🔸", ansi_dim)
                elif 30 < since <= 40:
                    ignite(cx, cy, code, " 🔸 ", "  ", ansi_off)
                elif since == 41:
                    ignite(cx, cy, code, "    ", "  ", ansi_off)
        return on_fire, cell_done

    def show_firewall(self, digger_xy: Tuple[int, int]) -> None:
        if digger_xy is not None:
            x, y = digger_xy
            self.__maze.maze_grid[y][x].visited_since = 1
            if digger_xy == self.__entry:
                cx = x * 6 + self.xoffset + 1
                cy = y * 3 + self.yoffset + 1
                self.grid.add_block(cx - 1, cy - 1, "  💣  ", Colors.RED)
                self.grid.add_block(cx - 1, cy, " 💣💣 ", Colors.RED)
                self.grid.add_block(cx - 1, cy + 1, "[0:04]", Colors.RED)
                self.grid.print_canvas()
                time.sleep(1)
                self.grid.add_block(cx - 1, cy + 1, "[0 03]", Colors.RED)
                self.grid.print_canvas()
                time.sleep(1)
                self.grid.add_block(cx - 1, cy + 1, "[0:02]", Colors.RED)
                self.grid.print_canvas()
                time.sleep(1)
                self.grid.add_block(cx - 1, cy + 1, "[0 01]", Colors.RED)
                self.grid.print_canvas()
                time.sleep(1)
                self.grid.add_block(cx - 1, cy + 1, "[0:00]", Colors.RED)
                self.grid.print_canvas()
                time.sleep(1)

        on_fire, cell_done = self.show_firewall_propagation()

        if cell_done >= self.__maze.width * self.__maze.height:
            while on_fire != 0:
                on_fire, _ = self.show_firewall_propagation()
                self.grid.print_canvas()
                time.sleep(1 / self.speed)

    def place_lowblocks_anim(self) -> None:
        x, _ = self.grid.center_block(" Generation steps ",
                                      x_start=1, x_end=self.xdim)
        self.left_panel_end = x
        self.grid.add_block(x - 1, self.ydim - 8,
                            "╤══════════════════╤", Colors.BROWN)
        for by in range(6):
            self.grid.add_block(x - 1, self.ydim - by - 2,
                                "│                  │", Colors.BROWN)
        self.grid.add_block(x - 1, self.ydim - 1,
                            "╧══════════════════╧", Colors.BROWN)
        self.grid.deco_zone(x, self.ydim - 7, x + 18, self.ydim - 2,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)
        self.grid.add_block(x, self.ydim - 7,
                            " Generation steps ", Colors.WHITE,
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
                            f"{self.speed:03d}", Colors.CYAN)
        dx = self.left_panel_end - 2 - len(self.color_theme_name)
        self.grid.add_block(dx, self.ydim - 5,
                            self.color_theme_name, Colors.CYAN)
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
                            Colors.CYAN, transparent=True)

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
                            self.color_theme_name, Colors.CYAN)

    def place_lowblocks_common(self) -> None:
        if self.__view == 2:
            self.right_panel_start = self.left_panel_end
        else:
            self.right_panel_start = self.left_panel_end + 18
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
        if self.exit_found == 1 and self.__maze.gen_step != 5:
            self.grid.add_block(x + 2, self.ydim - 5, "👑", Colors.EXIT)
        if self.exit_found == 1 and self.__maze.gen_step == 5:
            self.grid.add_block(x + 2, self.ydim - 5, "🪨", Colors.EXIT)
        txt = (f"{self.__width} x {self.__height} "
               f"({self.__width * self.__height})")
        if len(txt) > 13:
            txt = (f"{self.__width}x{self.__height}"
                   f"({self.__width * self.__height})")
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 7, txt, Colors.CYAN)
        ex, ey = self.__entry
        txt = f"{ex}, {ey}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 6, txt, Colors.CYAN)
        ex, ey = self.__exit
        txt = f"{ex}, {ey}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 5, txt, Colors.CYAN)
        txt = f"{self.__perfect}"
        dx = x + 28 - len(txt)
        self.grid.add_block(dx, self.ydim - 4, txt, Colors.CYAN)
        txt = f"{self.__seed}"
        if len(txt) <= 16:
            dx = x + 28 - len(txt)
            self.grid.add_block(dx, self.ydim - 3, txt, Colors.CYAN)
        else:
            mid = len(txt) // 2
            txt1 = txt[:mid]
            txt2 = txt[mid:]
            dx1 = x + 28 - len(txt1)
            dx2 = x + 28 - len(txt2)
            self.grid.add_block(dx1, self.ydim - 3, txt1, Colors.CYAN)
            self.grid.add_block(dx2, self.ydim - 2, txt2, Colors.CYAN)

    def place_lower_blocks(self) -> None:
        x, y = self.grid.center_block("", x_start=1, x_end=self.xdim)
        self.left_panel_end = x
        self.grid.deco_zone(2, self.ydim - 7, self.xdim - 2, self.ydim - 2,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)
        if self.__view == 3:
            self.place_lowblocks_anim()
        if self.__view == 2 or self.__maze.gen_step >= 3:
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
                elif self.__maze.gen_step >= 3:
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
                                "  ", Colors.EXIT)
        else:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "👑", Colors.EXIT)

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
            self.show_digger(self.digger_xy)
        elif self.digger_xy is not None and self.__algo == "prim":
            self.show_firewall(self.digger_xy)

    def collapse_wall(self, maze: Maze) -> None:
        if maze.active_cell:
            cell_x, cell_y, wall_code = maze.active_cell
        else:
            cell_x, cell_y, wall_code = 0, 0, 0
        ansi_off = self.grid.color_wall_ground(0)
        interval = 1 / self.speed
        gx = cell_x * 6 + self.xoffset
        gy = cell_y * 3 + self.yoffset
        if wall_code == 2:
            wx = gx + 5
            wy = gy
            self.grid.add_block(wx, wy, ["██", "▐▌", "██"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▜▛", "▕▏", "▟▙"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▜▛", "  ", "▟▙"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▀▀", "  ", "▄▄"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
        elif wall_code == 4:
            wx = gx + 1
            wy = gy + 2
            self.grid.add_block(wx, wy, ["▄▂▂▄", "▀▔▔▀"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▂  ▂", "▔▔▔▔"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▁  ▁", "▔  ▔"], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["    ", "    "], ansi_off)
            self.grid.print_canvas()
            time.sleep(interval)

    def light_path_cell(self, maze: Maze, mx: int, my: int, prev: str) -> None:
        cell = f"{self.__maze.maze_grid[my][mx].view_cell()}"
        code = int(cell, 16)
        ansi_dim = self.grid.color_wall_ground(1)
        ansi_lit = self.grid.color_wall_ground(2)

        def light_zone(xbase: int, ybase: int, ansi: str) -> None:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_canvas_cell(xbase + lx, ybase + ly, ansi)

        if (not code & 1 and prev != "S"
           and self.__maze.maze_grid[my - 1][mx].locked is False):
            light_zone(mx * 6 + self.xoffset,
                       (my - 1) * 3 + self.yoffset, ansi_dim)
        if (not code & 2 and prev != "W"
           and self.__maze.maze_grid[my][mx + 1].locked is False):
            light_zone((mx + 1) * 6 + self.xoffset,
                       my * 3 + self.yoffset, ansi_dim)
        if (not code & 4 and prev != "N"
           and self.__maze.maze_grid[my + 1][mx].locked is False):
            light_zone(mx * 6 + self.xoffset,
                       (my + 1) * 3 + self.yoffset, ansi_dim)
        if (not code & 8 and prev != "E"
           and self.__maze.maze_grid[my][mx - 1].locked is False):
            light_zone((mx - 1) * 6 + self.xoffset,
                       my * 3 + self.yoffset, ansi_dim)
        light_zone(mx * 6 + self.xoffset,
                   my * 3 + self.yoffset, ansi_lit)

    def show_path(self, maze: Maze) -> None:
        path = maze.shortest_path
        xin, yin = maze.entry
        self.light_path_cell(maze, xin, yin, "")
        x, y = xin, yin
        for direction in path:
            if direction == "N":
                y -= 1
            elif direction == "S":
                y += 1
            elif direction == "E":
                x += 1
            elif direction == "W":
                x -= 1
            self.light_path_cell(maze, x, y, direction)
        if self.__view == 3:
            self.anim_raider(maze)

    def anim_raider(self, maze: Maze) -> None:
        path = maze.shortest_path
        ansi_lit = self.grid.color_wall_ground(2)
        x, y = maze.entry
        x_entry, y_entry = x * 6 + self.xoffset + 2, y * 3 + self.yoffset + 1
        x, y = maze.exit
        x_exit, y_exit = x * 6 + self.xoffset + 2, y * 3 + self.yoffset + 1
        self.grid.print_canvas()
        time.sleep(1)
        x_raider, y_raider = x_entry, y_entry
        self.grid.add_block(x_raider, y_raider, "🤠", ansi_lit)
        self.grid.print_canvas()
        time.sleep(1)
        for direction in path:
            self.grid.add_block(x_entry, y_entry, "🚪", ansi_lit)
            go_x, go_y, go_offset = 0, 0, 0
            if direction == "N":
                go_y = -1
            elif direction == "S":
                go_y = 1
            elif direction == "E":
                go_x = 2
                go_offset = -1
            elif direction == "W":
                go_x = -2
                go_offset = 1
            for _ in range(3):
                if x_raider != x_entry or y_raider != y_entry:
                    self.grid.add_block(x_raider, y_raider, "  ", ansi_lit)
                x_raider, y_raider = x_raider + go_x, y_raider + go_y
                if x_raider == x_exit and y_raider == y_exit:
                    x_raider, y_raider = x_raider - go_x, y_raider - go_y
                else:
                    self.grid.add_block(x_raider, y_raider, "🤠", ansi_lit)
                    self.grid.print_canvas()
                    time.sleep(1 / self.speed)

        time.sleep(1)
        if go_offset != 1:
            self.grid.add_block(x_raider - 1 + go_offset, y_raider,
                                "🪨🤠", ansi_lit)
            self.grid.print_canvas()
            time.sleep(1)
            self.grid.add_block(x_raider - 1 + go_offset, y_raider,
                                "👑🤠", ansi_lit)
        else:
            self.grid.add_block(x_raider - 1 + go_offset, y_raider,
                                "🤠🪨", ansi_lit)
            self.grid.print_canvas()
            time.sleep(1)
            self.grid.add_block(x_raider - 1 + go_offset, y_raider,
                                "🤠👑", ansi_lit)
        self.grid.add_block(x_exit, y_exit, "🪨", ansi_lit)
        self.grid.add_block(self.right_panel_start + 2, self.ydim - 5,
                            "🪨", Colors.EXIT)
        self.grid.print_canvas()
        time.sleep(1)
        self.grid.add_block(x_raider - 1 + go_offset, y_raider,
                            "    ", ansi_lit)
        x_raider, y_raider = x_exit, y_exit
        self.grid.add_block(x_raider, y_raider, "🤠", ansi_lit)
        self.grid.add_block(x_exit, y_exit, "🪨", ansi_lit)
        self.grid.print_canvas()
        time.sleep(1 / self.speed)

        path = path[::-1]
        for direction in path:
            self.grid.add_block(x_exit, y_exit, "🪨", ansi_lit)
            go_x, go_y = 0, 0
            if direction == "N":
                go_y = 1
            elif direction == "S":
                go_y = -1
            elif direction == "E":
                go_x = -2
            elif direction == "W":
                go_x = 2
            for _ in range(3):
                if x_raider != x_exit or y_raider != y_exit:
                    self.grid.add_block(x_raider, y_raider, "  ", ansi_lit)
                x_raider, y_raider = x_raider + go_x, y_raider + go_y
                self.grid.add_block(x_raider, y_raider, "🤠", ansi_lit)
                self.grid.add_block(x_exit, y_exit, "🪨", ansi_lit)
                self.grid.print_canvas()
                time.sleep(1 / self.speed)
        time.sleep(1)
        self.grid.add_block(x_entry, y_entry, "🚪", ansi_lit)
        self.grid.print_canvas()
        time.sleep(1)
        x, y = self.grid.center_block("👑🤠👍", x_start=1,
                                      x_end=self.xdim)
        self.grid.add_block(x - 2, 7, "👑🤠👍", "")

        maze.gen_step = 5

    def render(self, maze: Maze, speed: int, algo: str,
               seed: Optional[str] = "",
               count_as_step: Optional[int] = 1) -> None:
        if maze.restart is True:
            self.previously_done = 0
            self.frame_count = 0
            maze.restart = False
        if self.previously_done == 1 and self.__maze.gen_step < 3:
            self.previously_done = 0
            self.frame_count = 0
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
                # self.grid.print_canvas()
                time.sleep(1)
            self.gen_step = 2
            self.collapse_wall(maze)
        elif self.__maze.gen_step == 4:
            self.show_path(maze)
        self.place_lower_blocks()
        self.grid.print_canvas()

    def change_color(self, new_color: int) -> None:
        self.color_theme += new_color
        if self.color_theme < 1:
            self.color_theme = 8
        if self.color_theme > 8:
            self.color_theme = 1
        self.grid.color_theme = self.color_theme
        self.grid.color_wall_ground(0)
