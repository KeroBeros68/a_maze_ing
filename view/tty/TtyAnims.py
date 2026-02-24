"""Animation rendering for TTY maze display.

This module handles visual animations for maze generation including digger
animation, firewall propagation, and other dynamic visual effects.

Classes:
    Anims: Manages animations for TTY maze visualization
"""

from view.tty.TtyUtils import Canvas
from view.tty.TtyView import TtyView
from view.tty.TtyLight import Light
from mazegen.maze.maze import Maze
from view.tty.TtyConsts import Colors, Elements
from typing import Tuple
import time
import random


class Anims:
    """Animation effects for maze generation visualization.

    Handles visual representation of maze generation process including
    the digger animation, firewall propagation, and other dynamic effects.
    """

    def __init__(self, view: TtyView, grid: Canvas, light: Light, maze: Maze,
                 viewmode: int) -> None:
        """Initialize the animation system.

        Args:
            view: TtyView instance
            grid: Canvas for rendering
            light: Light effects handler
            maze: The Maze object being animated
            viewmode: Display mode identifier
        """
        self.view = view
        self.grid = grid
        self.light = light
        self.__maze = maze
        self.__viewmode = viewmode
        self.x1 = self.view.xoffset
        self.y1 = self.view.yoffset
        self.x2 = self.__maze.width * 6 + self.x1
        self.y2 = self.__maze.height * 3 + self.y1

    def show_digger(self, digger_xy: Tuple[int, int]) -> None:
        ex, ey = self.__maze.entry
        self.light.light_cell(x=ex, y=ey, lit_max=1.0, dim_lit=0.5)
        x, y = digger_xy
        self.grid.add_block(x * 6 + self.view.xoffset + 1,
                            y * 3 + self.view.yoffset + 1, "🔨🧔",
                            "")
        self.light.light_cell(x=x, y=y, lit_max=3.0, dim_lit=0.165)

    def show_firewall_propagation(self) -> tuple[int, int]:
        on_fire = 0
        cell_done = 0
        self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)

        def ignite(x: int, y: int, code: int, center: str,
                   sides: str, lit: float) -> None:
            cx = x * 6 + self.view.xoffset + 1
            cy = y * 3 + self.view.yoffset + 1
            if lit == 0:
                lit = 0.1
            self.grid.add_block(cx, cy, f"{center}")
            self.light.light_cell(x=x, y=y, lit_max=lit,
                                  dim_lit=1 / (2 * lit))
            if not code & 1:
                self.grid.add_block(cx, cy - 1, f"{sides}{sides}")
            if not code & 4:
                self.grid.add_block(cx, cy + 1, f"{sides}{sides}")
            if not code & 2:
                self.grid.add_block(cx + 4, cy, f"{sides}")
            if not code & 8:
                self.grid.add_block(cx - 2, cy, f"{sides}")
            self.light.light_cell(x=x, y=y, lit_max=lit,
                                  dim_lit=1 / (2 * lit))

        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                since = self.__maze.maze_grid[y][x].visited_since
                if since > 0:
                    self.__maze.maze_grid[y][x].visited_since = since + 1
                if 0 < since <= 50:
                    on_fire += 1
                if (self.__maze.maze_grid[y][x].visited is True
                   or self.__maze.maze_grid[y][x].locked is True):
                    cell_done += 1
                cell = f"{self.__maze.maze_grid[y][x].view_cell()}"
                code = int(cell, 16)
                since = self.__maze.maze_grid[y][x].visited_since
                if 0 < since <= 5:
                    ignite(x, y, code, " 💥 ", "🔥", 4.0)
                elif 5 < since <= 20:
                    ignite(x, y, code, "🔥🔥", "🔥", 2.0)
                elif 20 < since <= 30:
                    ignite(x, y, code, " 🔥 ", "🔸", 1.0)
                elif 30 < since <= 40:
                    ignite(x, y, code, " 🔸 ", "  ", 0.5)
                elif since == 41:
                    ignite(x, y, code, "    ", "  ", 0.25)
        return on_fire, cell_done

    def show_firewall(self, digger_xy: Tuple[int, int]) -> None:
        if digger_xy is not None:
            x, y = digger_xy
            self.__maze.maze_grid[y][x].visited_since = 1
            if digger_xy == self.__maze.entry:
                cx = x * 6 + self.view.xoffset + 1
                cy = y * 3 + self.view.yoffset + 1
                self.grid.add_block(cx - 1, cy - 1, "  💣  ", Colors.RED)
                self.grid.add_block(cx - 1, cy, " 💣💣 ", Colors.RED)
                count_start = 5
                for i in range(count_start):
                    self.grid.add_block(cx - 1, cy + 1,
                                        f"[0:0{count_start - i - 1}]",
                                        Colors.RED)
                    self.grid.print_canvas()
                    time.sleep(0.5)
                    self.grid.add_block(cx + 1, cy + 1, " ", Colors.RED)
                    self.grid.print_canvas()
                    time.sleep(0.5)

        on_fire, cell_done = self.show_firewall_propagation()

        if cell_done >= self.__maze.width * self.__maze.height:
            while on_fire != 0:
                on_fire, _ = self.show_firewall_propagation()
                self.grid.print_canvas()
                time.sleep(1 / self.view.speed)

    def collapse_wall(self, maze: Maze) -> None:
        if maze.active_cell:
            cell_x, cell_y, wall_code = maze.active_cell
        else:
            cell_x, cell_y, wall_code = 0, 0, 0
        interval = 1 / self.view.speed
        gx = cell_x * 6 + self.view.xoffset
        gy = cell_y * 3 + self.view.yoffset
        rnd = random.randrange(2)
        if wall_code == 2:
            self.light.light_cell_from_xy(gx, gy, 0.25)
            self.light.light_cell_from_xy(gx + 6, gy, 0.25)
            wx = gx + 5
            wy = gy
            self.grid.add_block(wx, wy, ["██", "▒▒", "██"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["█▛", "▒▒", "▟█"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▜▛", "▒▒", "▟▙"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▀▀", "░░", "▄▄"])
            self.grid.print_canvas()
            time.sleep(interval)
        elif wall_code == 4 and rnd == 1:
            self.light.light_cell_from_xy(gx, gy, 0.25)
            self.light.light_cell_from_xy(gx, gy + 3, 0.25)
            wx = gx + 1
            wy = gy + 2
            self.grid.add_block(wx, wy, ["▄▒▒▄", "▀▔▔▀"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▂▒▒▂", "▔▔▔▔"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▁▒▒▁", "▔  ▔"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["░░░░", "    "])
            self.grid.print_canvas()
            time.sleep(interval)
        elif wall_code == 4 and rnd == 0:
            self.light.light_cell_from_xy(gx, gy, 0.25)
            self.light.light_cell_from_xy(gx, gy + 3, 0.25)
            wx = gx + 1
            wy = gy + 2
            self.grid.add_block(wx, wy, ["▄▂▂▄", "▀▒▒▀"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▂▂▂▂", "▔▒▒▔"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["▁▁▁▁", "▔▒▒▔"])
            self.grid.print_canvas()
            time.sleep(interval)
            self.grid.add_block(wx, wy, ["    ", "░░░░"])
            self.grid.print_canvas()
            time.sleep(interval)

    def anim_raider(self, maze: Maze) -> None:
        path = maze.shortest_path
        x, y = maze.entry
        x_entry = x * 6 + self.view.xoffset + 2
        y_entry = y * 3 + self.view.yoffset + 1
        x, y = maze.exit
        x_exit = x * 6 + self.view.xoffset + 2
        y_exit = y * 3 + self.view.yoffset + 1
        self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
        self.grid.print_canvas()
        time.sleep(1)
        self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)
        self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
        x_raider, y_raider = x_entry, y_entry
        self.grid.add_block(x_raider, y_raider, "🤠")
        self.light.light_cell_from_xy(x_raider, y_raider, 1.5)

        x = self.view.left_panel_end
        r, g, b, _, _, _ = self.grid.color_wall_ground_raw(1)
        r = min(255, r * 2)
        g = min(255, g * 2)
        b = min(255, b * 2)
        ansi = f"\33[38;2;{r};{g};{b}m\33[48;2;0;0;0m"
        self.grid.deco_zone(x, self.view.ydim - 7, x + 19, self.view.ydim - 2,
                            Elements.DECO_FILL, Colors.DEEP_BROWN)
        self.grid.add_block(x, self.view.ydim - 7, Elements.TATADATAAA,
                            ansi, transparent=True)

        self.grid.print_canvas()
        time.sleep(1)
        self.grid.add_block(x_raider - 1, y_raider, "📓🤠")
        self.light.light_cell_from_xy(x_raider, y_raider, 2.0)
        self.grid.print_canvas()
        time.sleep(1)
        self.view.show_path()
        self.grid.print_canvas()
        time.sleep(1)
        x_raider, y_raider = x_entry, y_entry
        self.grid.add_block(x_raider - 1, y_raider, " 🤠 ")
        self.light.light_cell_from_xy(x_raider, y_raider, 1.5)
        self.grid.print_canvas()
        time.sleep(0.5)
        self.grid.add_block(x_raider - 1, y_raider, "🔦🤠")
        self.light.light_cell_from_xy(x_raider, y_raider, 3.0)
        self.grid.print_canvas()
        time.sleep(1)
        for direction in path:
            self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)
            self.grid.add_block(x_entry - 1, y_entry, " 🚪 ")
            self.view.show_path()
            self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
            self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
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
                    self.grid.add_block(x_raider - 1, y_raider, "    ")
                    self.light.light_cell_from_xy(x_raider, y_raider, 1.0)
                x_raider, y_raider = x_raider + go_x, y_raider + go_y
                if y_raider == y_exit and abs(x_raider - x_exit) <= 2:
                    x_raider, y_raider = x_raider - go_x, y_raider - go_y
                else:
                    self.view.show_path()
                    self.grid.add_block(x_raider - 1, y_raider, "🔦🤠")
                    self.grid.add_block(x_entry - 1, y_entry, " 🚪 ")
                    self.light.light_cell_from_xy(x_raider, y_raider, 3.0)
                    self.grid.print_canvas()
                    time.sleep(1 / self.view.speed)

        time.sleep(1)
        if go_offset != 1 and x_raider <= x_exit:
            self.grid.add_block(x_raider - 1 - go_offset, y_raider,
                                "🪨🤠")
            self.grid.print_canvas()
            time.sleep(1)
            self.grid.add_block(x_raider - 1 - go_offset, y_raider,
                                "👑🤠")
        else:
            self.grid.add_block(x_raider - 1 - go_offset, y_raider,
                                "🤠🪨")
            self.grid.print_canvas()
            time.sleep(1)
            self.grid.add_block(x_raider - 1 - go_offset, y_raider,
                                "🤠👑")
        self.grid.add_block(x_exit, y_exit, "🪨")
        self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
        self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
        self.grid.add_block(self.view.right_panel_start + 2,
                            self.view.ydim - 5,
                            "🪨", Colors.EXIT)
        self.grid.print_canvas()
        time.sleep(1)
        self.grid.add_block(x_raider - 1 + go_offset, y_raider,
                            "    ")
        self.light.light_cell_from_xy(x_raider, y_raider, 1.0)
        x_raider, y_raider = x_exit, y_exit
        self.grid.add_block(x_raider, y_raider, "🤠")
        self.light.light_cell_from_xy(x_raider, y_raider, 3.0)
        self.grid.add_block(x_exit, y_exit, "🪨")
        self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
        self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
        self.grid.print_canvas()
        time.sleep(1 / self.view.speed)

        path = path[::-1]
        for direction in path:
            self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)
            self.grid.add_block(x_exit - 1, y_exit, " 🪨 ")
            self.view.show_path()
            self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
            self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
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
                    self.grid.add_block(x_raider - 1, y_raider, "    ")
                    self.light.light_cell_from_xy(x_raider, y_raider, 1.0)
                x_raider, y_raider = x_raider + go_x, y_raider + go_y
                self.view.show_path()
                if y_raider == y_entry and abs(x_raider - x_entry) <= 2:
                    self.grid.add_block(x_entry - 1, y_entry, "    ")
                else:
                    self.grid.add_block(x_entry - 1, y_entry, " 🚪 ")
                self.grid.add_block(x_raider - 1, y_raider, "🔦🤠")
                self.light.light_cell_from_xy(x_raider, y_raider, 3.0)
                if y_raider == y_exit and abs(x_raider - x_exit) <= 2:
                    self.grid.add_block(x_exit - 1, y_exit, "    ")
                else:
                    self.grid.add_block(x_exit - 1, y_exit, " 🪨 ")
                self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
                self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
                self.grid.print_canvas()
                time.sleep(1 / self.view.speed)

        time.sleep(1)
        self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)
        self.grid.add_block(x_raider - 1, y_raider, "👋🤠")
        self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
        self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
        self.light.light_cell_from_xy(x_raider, y_raider, 2.0)
        self.grid.print_canvas()
        time.sleep(1)
        self.light.reset_light_zone(self.x1, self.y1, self.x2, self.y2)
        self.grid.add_block(x_entry - 1, y_entry, " 🚪 ")
        self.light.light_cell_from_xy(x_entry, y_entry, 1.0)
        self.light.light_cell_from_xy(x_exit, y_exit, 1.0)
        self.grid.print_canvas()
        time.sleep(1)
        x, y = self.grid.center_block("👑🤠👍", x_start=1,
                                      x_end=self.view.xdim)
        self.grid.add_block(x - 2, 7, "👑🤠👍", "")

        maze.gen_step = 5
