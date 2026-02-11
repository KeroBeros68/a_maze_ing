from mazegen.maze.maze import Maze
from model.Model import ConfigModel
from dataclasses import dataclass
from typing import List, Iterable, Tuple, Optional, Callable
import time
import sys
import unicodedata
import termios
import tty
import select
import atexit
import os

LEFT_BANNER = [
    " ◢◤ ◤█",
    "◢◤  ◢◤",
    "███ █◢",
    "  █   ",
    " 2026 ",
    "      ",
    "      ",
    " OPR  ",
]
RIGHT_BANNER = [
    "█◥ ◥◣ ",
    "◥◣  ◥◣",
    "◣█ ███",
    "   █  ",
    " 2026 ",
    "      ",
    "      ",
    " Kero ",
]
CENTER_BANNER = [
    "    ▁▁▁           ▁▁  ▁▁▁                         ▁▁           ",
    "   ╱   │         ╱  │╱  ╱▁▁▁▁▁▁▁▁▁  ▁▁▁          ╱▁╱▁▁▁  ▁▁▁▁▁▁",
    "  ╱ ╱│ │ ▁▁▁▁▁▁ ╱ ╱│▁╱ ╱ ▁▁  ╱▁  ╱ ╱ ▁ ╲ ▁▁▁▁▁▁ ╱ ╱ ▁▁ ╲╱ ▁▁  ╱",
    " ╱ ▁▁▁ │╱▁▁▁▁▁╱╱ ╱  ╱ ╱ ╱▁╱ ╱ ╱ ╱▁╱  ▁▁╱╱▁▁▁▁▁╱╱ ╱ ╱ ╱ ╱ ╱▁╱ ╱ ",
    "╱▁╱  │▁│      ╱▁╱  ╱▁╱╲▁▁▁▁╱ ╱▁▁▁╱╲▁▁▁╱       ╱▁╱▁╱ ╱▁╱╲▁▁  ╱  ",
    "                                                      ╱▁▁▁▁╱   ",
]
SIGNATURE_BANNER = "   42 - orobert & kebertra - 2025"
SIGNATURE_COLORS = "000660305555555030555555550306666"
ANIM_LEFT_PANEL = [
    " Space/P : Pause            ",
    " +/-     : Speed            ",
    " C/V     : Color            ",
    " ESC/Q   : Exit             ",
]
LEFT_PANEL = [
    " F       : Show path        ",
    " R       : Regenerate       ",
    " C/V     : Color            ",
    " ESC/Q   : Exit             ",
]
RIGHT_PANEL = [
    " Maze size :                 ",
    " 🚪 Entry  :                 ",
    " 👑 Exit   :                 ",
    " Perfect   :                 ",
]
LARGE_DIGITS = [
    "┏━┓╺┓ ┏━┓┏━┓╻ ╻┏━╸┏━┓┏━┓┏━┓┏━┓",
    "┃ ┃ ┃ ┏━┛ ╺┫┗━┫┗━┓┣━┓  ┃┣━┫┗━┫",
    "┗━┛╺┻╸┗━╸┗━┛  ╹┗━┛┗━┛  ╹┗━┛┗━┛",
]
CLOSED_CELL = [
    "▒▒▒▒▒▒",
    "▒▒░░▒▒",
    "▒▒▒▒▒▒",
]
DECO_FILL = [
    "──┘ │ ├─",
    "┌─╴ ╵ │ ",
    "│ ┌─╴ ╵ ",
    "└─┤ ┌─┐ ",
]

BLACK = "\33[30m"
RED = "\33[31m"
GREEN = "\33[32m"
BROWN = "\33[33m"
PURPLE = "\33[35m"
CYAN = "\33[36m"
WHITE = "\33[37m"
BLUE42 = "\33[38;2;16;32;96m"
DEEP_PURPLE = "\33[38;2;54;18;72m"
DEEP_BROWN = "\33[38;2;60;45;30m"
CLOSED = "\33[38;2;32;16;8m"
ENTRY = "\33[38;5;45m"
EXIT = "\33[38;5;208m"

RESET = "\33[0;1;37m"


class KeyPoller:
    def __init__(self) -> None:
        self.fd = None
        self.old = None
        self.enabled = False

    def start(self) -> None:
        if self.enabled:
            return
        self.fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        self.enabled = True

    def stop(self) -> None:
        if not self.enabled:
            return
        assert self.fd is not None and self.old is not None
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)
        self.enabled = False

    def poll(self) -> str | None:
        if not self.enabled:
            return None
        r, _, _ = select.select([sys.stdin], [], [], 0)
        if r:
            return sys.stdin.read(1)
        return None

    def exit_program(self) -> None:
        KEYS.stop()
        restore_terminal()
        sys.exit(0)


KEYS = KeyPoller()


def restore_terminal() -> None:
    try:
        KEYS.stop()
    finally:
        os.system("stty sane")
        sys.stdout.write("\33[?25h\33[0m\n")
        sys.stdout.flush()


atexit.register(restore_terminal)


@dataclass(slots=True)
class TermCell:
    ch: str = " "
    color: str = ""
    cont: bool = False


class TermGrid:
    def __init__(
            self,
            width: int,
            height: int,
            color_wall_ground: Callable[[int], str],
            default: TermCell | None = None
            ) -> None:
        self.width = width
        self.height = height
        self.color_wall_ground = color_wall_ground or (lambda _lvl: "")
        base = default if default is not None else TermCell(" ", "")
        self._grid: List[List[TermCell]] = [
            [TermCell(base.ch, base.color) for _ in range(width)]
            for _ in range(height)
        ]

    @staticmethod
    def term_width(s: str) -> int:
        if not s:
            return 0
        o = ord(s)
        if 0xFE00 <= o <= 0xFE0F:
            return 0
        if unicodedata.combining(s):
            return 0
        eaw = unicodedata.east_asian_width(s)
        if eaw in ("W", "F"):
            return 2
        if (
            0x1F300 <= o <= 0x1FAFF   # pictos / emojis
            or 0x2600 <= o <= 0x26FF  # misc symbols
            or 0x2700 <= o <= 0x27BF  # dingbats
        ):
            return 2
        return 1

    def set_cell(self, x: int, y: int, ch: str, color: str = "") -> None:
        self._grid[y][x].ch = ch
        self._grid[y][x].color = color
        self._grid[y][x].cont = False
        char_width = self.term_width(ch)
        if char_width == 2 and x + 1 < self.width:
            self._grid[y][x + 1].ch = ""
            self._grid[y][x + 1].color = ""
            self._grid[y][x + 1].cont = True

    def color_cell(self, x: int, y: int, color: str = "") -> None:
        self._grid[y][x].color = color

    def get_cell(self, x: int, y: int) -> TermCell:
        return self._grid[y][x]

    def clear(self, ch: str = " ", color: str = "") -> None:
        for y in range(self.height):
            row = self._grid[y]
            for x in range(self.width):
                row[x].ch = ch
                row[x].color = color
                row[x].cont = False

    def measure_block(self, block: str | Iterable[str]) -> tuple[int, int]:
        if isinstance(block, str):
            lines = block.splitlines()
        else:
            lines = list(block)
        if not lines:
            return (0, 0)
        width = max(len(line) for line in lines)
        height = len(lines)
        return (width, height)

    def center_block(
        self,
        block: str | list[str],
        x_start: int = 0,
        x_end: int = 0,
        y_start: int = 0,
        y_end: int = 0,
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> tuple[int, int]:
        bw, bh = self.measure_block(block)
        xs = max(0, min(self.width, x_start))
        xe = max(0, min(self.width, x_end))
        ys = max(0, min(self.height, y_start))
        ye = max(0, min(self.height, y_end))
        if xe < xs:
            xs, xe = xe, xs
        if ye < ys:
            ys, ye = ye, ys
        zone_w = max(0, xe - xs)
        zone_h = max(0, ye - ys)
        x = xs + (zone_w - bw) // 2 + offset_x
        y = ys + (zone_h - bh) // 2 + offset_y
        return (x, y)

    def deco_zone(self, x1: int, y1: int, x2: int, y2: int,
                  source: str | Iterable[str], color: str = "") -> None:
        if x2 < x1:
            return
        if y2 < y1:
            return
        width: int = x2 - x1 + 1
        height: int = y2 - y1 + 1
        if isinstance(source, str):
            src_lines = source.splitlines()
        else:
            src_lines = list(source)
        if not src_lines:
            return
        src_h = len(src_lines)
        src_w = max((len(line) for line in src_lines), default = 0)
        if src_w == 0:
            return
        for dy in range(height):
            sy = dy % src_h
            motif_line = src_lines[sy]
            if not motif_line:
                continue
            reps = (width + len(motif_line) - 1) // len(motif_line)
            tiled = (motif_line * reps)[:width]
            self.add_block(x1, y1 + dy, tiled, color)

    def add_block(
                self,
                x: int,
                y: int,
                block: str | Iterable[str],
                color: str = "",
                transparent: bool = False,
                transparent_chars: set[str] | None = None,
            ) -> None:
        if isinstance(block, str):
            lines = block.splitlines()
        else:
            lines = list(block)
        if transparent_chars is None:
            transparent_chars = {" "}
        for dy, line in enumerate(lines):
            if not line:
                continue
            gy = y + dy
            if gy < 0 or gy >= self.height:
                continue
            gx = x
            for ch in line:
                char_width = self.term_width(ch)
                if char_width == 0:
                    continue
                if transparent and ch in transparent_chars:
                    gx += char_width
                    if gx >= self.width:
                        break
                    continue
                if 0 <= gx < self.width:
                    self.set_cell(gx, gy, ch, color)
                gx += char_width
                if gx >= self.width:
                    break

    def add_cell(self, x: int, y: int, cell: str):
        code = int(cell, 16)
        ansi = self.color_wall_ground(0)
        ansi_closed = self.color_wall_ground(-1)
        if code == 15:
            self.add_block(x, y, CLOSED_CELL, ansi_closed)
            return
        self.add_block(x, y, "▀", ansi)
        self.add_block(x + 5, y, "▀", ansi)
        self.add_block(x, y + 2, "▄", ansi)
        self.add_block(x + 5, y + 2, "▄", ansi)
        if code & 1:
            self.add_block(x + 1, y, "▀▀▀▀", ansi)
        if code & 2:
            for cy in range(3):
                self.add_block(x + 5, y + cy, "█", ansi)
        if code & 4:
            self.add_block(x + 1, y + 2, "▄▄▄▄", ansi)
        if code & 8:
            for cy in range(3):
                self.add_block(x, y + cy, "█", ansi)
#        self.add_block(x, y, "█▀", ansi)
#        self.add_block(x + 4, y, "▀█", ansi)
#        self.add_block(x, y + 2, "█▄", ansi)
#        self.add_block(x + 4, y + 2, "▄█", ansi)
#        if code & 1:
#            self.add_block(x + 2, y, "▀▀", ansi)
#        if code & 2:
#            self.add_block(x + 5, y + 1, "█", ansi)
#        if code & 4:
#            self.add_block(x + 2, y + 2, "▄▄", ansi)
#        if code & 8:
#            self.add_block(x, y + 1, "█", ansi)

    def render(self, reset_each_cell: bool = True) -> str:
        lines: List[str] = []
        if reset_each_cell:
            for y in range(self.height):
                rows_in_line: List[str] = []
                for x in range(self.width):
                    cell = self._grid[y][x]
                    if cell.cont:
                        continue
                    if cell.color:
                        rows_in_line.append(f"{cell.color}{cell.ch}{RESET}")
                    else:
                        rows_in_line.append(cell.ch)
                lines.append("".join(rows_in_line))
        else:
            for y in range(self.height):
                rows_in_line = []
                for x in range(self.width):
                    cell = self._grid[y][x]
                    if cell.cont:
                        continue
                    if cell.color:
                        rows_in_line.append(f"{cell.color}{cell.ch}")
                    else:
                        rows_in_line.append(cell.ch)
                lines.append("".join(rows_in_line) + RESET)
        return "\n".join(lines)

    def print(self) -> None:
        sys.stdout.write("\33[H\33[?25l\33[1m\n")
        sys.stdout.write(self.render())
        sys.stdout.flush()

    def template(self) -> None:
        for x in range(self.width):
            if x > 0:
                self.set_cell(x, 0, "═", BROWN)
                self.set_cell(x, 9, "═", BROWN)
                self.set_cell(x, self.height - 6, "═", BROWN)
                self.set_cell(x, self.height - 1, "═", BROWN)
        for y in range(self.height):
            self.set_cell(1, y, "║", BROWN)
            self.set_cell(self.width - 1, y, "║", BROWN)
        self.set_cell(1, 0, "╔", BROWN)
        self.set_cell(self.width - 1, 0, "╗", BROWN)
        self.set_cell(1, self.height - 1, "╚", BROWN)
        self.set_cell(self.width - 1, self.height - 1, "╝", BROWN)
        self.set_cell(1, 9, "╠", BROWN)
        self.set_cell(1, self.height - 6, "╠", BROWN)
        self.set_cell(self.width - 1, 9, "╣", BROWN)
        self.set_cell(self.width - 1, self.height - 6, "╣", BROWN)
        self.deco_zone(2, 1, self.width - 2, 8, DECO_FILL, DEEP_PURPLE)
        self.add_block(2, 1, LEFT_BANNER, BLUE42, transparent = True)
        self.add_block(self.width - 7, 1, RIGHT_BANNER, BLUE42,
                       transparent = True)
        x, y = self.center_block(CENTER_BANNER,
                                 x_start=8, x_end=self.width - 7)
        self.add_block(x, 1, CENTER_BANNER, PURPLE, transparent = True)
        bx, by = self.measure_block(CENTER_BANNER)
        x, y = self.center_block(SIGNATURE_BANNER,
                                 x_start=8, x_end=self.width - 7)
        self.add_block(x, 8, SIGNATURE_BANNER, BROWN, transparent = True)
        for i in range(len(SIGNATURE_COLORS)):
            if SIGNATURE_COLORS[i] is not "0":
                color = f"\33[3{SIGNATURE_COLORS[i]}m"
                self.color_cell(x + i, 8, color)


class TermView:
    frame_count = 1
    exit_found = 0
    quit_requested = False
    paused = False
    speed = 15
    left_panel_end = 0
    color_theme = 1

    def __init__(self, config: ConfigModel, maze: Maze):
        self.__config = config
        self.__width = config.WIDTH
        self.__height = config.HEIGHT
        self.__entry = config.ENTRY
        self.__exit = config.EXIT
        self.__seed = config.SEED
        self.__view = config.VIEW
        self.__perfect = config.PERFECT
        self.__maze = maze
        self.xoffset = 2
        self.xdim = (self.__width * 6) + 3
        xl, yl = TermGrid.measure_block(TermGrid, LEFT_BANNER)
        xc, yc = TermGrid.measure_block(TermGrid, CENTER_BANNER)
        xr, yr = TermGrid.measure_block(TermGrid, RIGHT_BANNER)
        if self.xdim < xl + xc + xr + 7:
            self.xoffset = max(0, int((xl + xc + xr + 7 - self.xdim) / 2 + 2))
            self.xdim = xl + xc + xr + 7
        self.ydim = (self.__height * 3) + 16
        self.yoffset = 10
        self.color_theme_name = "Cave"
        self.grid = TermGrid(self.xdim, self.ydim,
                             color_wall_ground=self.color_wall_ground)

    @staticmethod
    def handle_key(key: str) -> None:
        if key in ("q", "Q", "\33"):
            TermView.quit_requested = True
            return
        if key in (" ", "p", "P"):
            TermView.paused = not TermView.paused
            return
        if key in ("+", "="):
            TermView.speed = min(120, TermView.speed * 2)
            return
        if key in ("-", "_"):
            TermView.speed = max(1, int(TermView.speed / 2))
            return
        if key in ("C", "c"):
            TermView.color_theme -= 1
            if TermView.color_theme < 1:
                TermView.color_theme = 5
        if key in ("V", "v"):
            TermView.color_theme += 1
            if TermView.color_theme > 5:
                TermView.color_theme = 1

    @staticmethod
    def large_counter_block(
        value: int,
        min_digits: int = 1,
        pad_char: str = "0",
    ) -> str:

        s = str(max(0, value))
        if len(s) < min_digits:
            s = s.rjust(min_digits, pad_char)
        block_lines = ["", "", ""]
        for ch in s:
            if "0" <= ch <= "9":
                d = ord(ch) - ord("0")
                start = d * 3
                end = start + 3
                block_lines[0] += LARGE_DIGITS[0][start:end]
                block_lines[1] += LARGE_DIGITS[1][start:end]
                block_lines[2] += LARGE_DIGITS[2][start:end]
            else:
                block_lines[0] += " " * 3
                block_lines[1] += " " * 3
                block_lines[2] += " " * 3
        return "\n".join(block_lines)

    def wait_for_quit(self) -> None:
        KEYS.start()
        while True:
            key = KEYS.poll()
            if key in ("C", "c", "V", "v"):
                if key in ("C", "c"):
                    TermView.color_theme -= 1
                    if TermView.color_theme < 1:
                        TermView.color_theme = 5
                if key in ("V", "v"):
                    TermView.color_theme += 1
                    if TermView.color_theme > 5:
                        TermView.color_theme = 1
                self.display_maze()
            if key in ("q", "Q", "\33"):
                break
            time.sleep(0.02)
        KEYS.exit_program()

    def color_wall_ground(self, lit: int) -> str:
        r, g, b = 96, 48, 24
        if TermView.color_theme == 1:
            r, g, b = 96, 48, 24
            self.color_theme_name = "Cave"
        elif TermView.color_theme == 2:
            r, g, b = 16, 64, 32
            self.color_theme_name = "Forest"
        elif TermView.color_theme == 3:
            r, g, b = 0, 91, 118
            self.color_theme_name = "Smurfy"
        elif TermView.color_theme == 4:
            r, g, b = 128, 64, 96
            self.color_theme_name = "CandyShop"
        elif TermView.color_theme == 5:
            r, g, b = 64, 32, 128
            self.color_theme_name = "DeepPurple"
        dr = int(r + ((r / 2) * lit))
        dg = int(g + ((g / 2) * lit))
        db = int(b + ((b / 2) * lit))
        dr = max(0, min(255, dr))
        dg = max(0, min(255, dg))
        db = max(0, min(255, db))
        gr = ""
        if lit == 1:
            gr = "\33[48;5;234m"
        if lit == 2:
            gr = "\33[48;5;238m"
        ansi = f"\33[38;2;{dr};{dg};{db}m{gr}"
        return ansi

    def show_digger(self, digger_xy: Tuple[int, int]) -> None:
        if digger_xy == self.__exit:
            TermView.exit_found = 1
        x, y = digger_xy
        self.grid.add_block(x * 6 + self.xoffset + 1,
                            y * 3 + self.yoffset + 1, "🔦🤠", PURPLE)
        cell = f"{self.__maze.maze_grid[y][x].view_cell()}"
        code = int(cell, 16)
        ansi_dim = self.color_wall_ground(1)
        ansi_lit = self.color_wall_ground(2)
        if not code & 1:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_cell(x * 6 + self.xoffset + lx,
                                         (y - 1) * 3 + self.yoffset + ly,
                                         ansi_dim)
        if not code & 2:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_cell((x + 1) * 6 + self.xoffset + lx,
                                         y * 3 + self.yoffset + ly, ansi_dim)
        if not code & 4:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_cell(x * 6 + self.xoffset + lx,
                                         (y + 1) * 3 + self.yoffset + ly,
                                         ansi_dim)
        if not code & 8:
            for ly in range(3):
                for lx in range(6):
                    self.grid.color_cell((x - 1) * 6 + self.xoffset + lx,
                                         y * 3 + self.yoffset + ly,
                                         ansi_dim)
        for ly in range(3):
            for lx in range(6):
                self.grid.color_cell(x * 6 + self.xoffset + lx,
                                     y * 3 + self.yoffset + ly,
                                     ansi_lit)

    def display_maze(self,
                     digger_xy: Optional[Tuple[int, int]] = None
                     ) -> None:
        KEYS.start()
        key = KEYS.poll()
        if key:
            TermView.handle_key(key)

        self.grid.clear(" ", "")
        self.grid.template()
        for y in range(self.__maze.height):
            for x in range(self.__maze.width):
                cell_view = f"{self.__maze.maze_grid[y][x].view_cell()}"
                self.grid.add_cell(x * 6 + self.xoffset, y * 3 + self.yoffset,
                                   cell_view)
        x, y = self.__entry
        self.grid.add_block(x * 6 + self.xoffset + 2,
                            y * 3 + self.yoffset + 1,
                            "🚪", ENTRY)
        x, y = self.__exit
        if TermView.exit_found == 0:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "👑", EXIT)
        else:
            self.grid.add_block(x * 6 + self.xoffset + 2,
                                y * 3 + self.yoffset + 1,
                                "🪨", EXIT)

        if digger_xy is not None:
            self.show_digger(digger_xy)
        elif self.__view == 3:
            x, y = self.grid.center_block("👑🤠👍", x_start=1, x_end=self.xdim)
            self.grid.add_block(x - 2, 7, "👑🤠👍", "")

        x, y = self.grid.center_block(" ", x_start=1, x_end=self.xdim)
        TermView.left_panel_end = x
        self.grid.deco_zone(2, self.ydim - 5, self.xdim - 2, self.ydim - 2,
                            DECO_FILL, DEEP_BROWN)
        if self.__view == 3:
            x, y = self.grid.center_block(" Generation steps ",
                                          x_start=1, x_end=self.xdim)
            TermView.left_panel_end = x
            self.grid.add_block(x - 1, self.ydim - 6,
                                "╤══════════════════╤", BROWN)
            for by in range(4):
                self.grid.add_block(x - 1, self.ydim - by - 2,
                                    "│                  │", BROWN)
            self.grid.add_block(x - 1, self.ydim - 1,
                                "╧══════════════════╧", BROWN)
            self.grid.add_block(x, self.ydim - 5,
                                " Generation steps ", WHITE)
            x -= 30
            self.grid.add_block(x, self.ydim - 6,
                                "╤════════════════════════════╤", BROWN)
            for by in range(4):
                self.grid.add_block(x, self.ydim - by - 2,
                                    "│                            │", BROWN)
            self.grid.add_block(x, self.ydim - 1,
                                "╧════════════════════════════╧", BROWN)
            self.grid.add_block(x + 1, self.ydim - 5, ANIM_LEFT_PANEL, WHITE)
            if TermView.paused:
                self.grid.add_block(TermView.left_panel_end - 10,
                                    self.ydim - 5, "[ACTIVE]", GREEN)
            self.grid.add_block(TermView.left_panel_end - 5, self.ydim - 4,
                                f"{TermView.speed:03d}", CYAN)
            dx = TermView.left_panel_end - 2 - len(self.color_theme_name)
            self.grid.add_block(dx, self.ydim - 3,
                                self.color_theme_name, CYAN)
            if TermView.exit_found == 0:
                self.grid.add_block(TermView.left_panel_end - 4,
                                    self.ydim - 2, "🪨", EXIT)
            elif digger_xy is not None:
                self.grid.add_block(TermView.left_panel_end - 4,
                                    self.ydim - 2, "👑", EXIT)
            frame_counter = self.large_counter_block(TermView.frame_count)
            x, y = self.grid.center_block(f"{frame_counter}",
                                          x_start=1, x_end=self.xdim)
            self.grid.add_block(x, self.ydim - 4, f"{frame_counter}", CYAN)

        if self.__view == 2 or digger_xy is None:
            x = TermView.left_panel_end - 30
            self.grid.add_block(x, self.ydim - 6,
                                "╤════════════════════════════╤", BROWN)
            for by in range(4):
                self.grid.add_block(x, self.ydim - by - 2,
                                    "│                            │", BROWN)
            self.grid.add_block(x, self.ydim - 1,
                                "╧════════════════════════════╧", BROWN)
            self.grid.add_block(x + 1, self.ydim - 5, LEFT_PANEL, WHITE)
            dx = TermView.left_panel_end - 2 - len(self.color_theme_name)
            self.grid.add_block(dx, self.ydim - 3,
                                self.color_theme_name, CYAN)

        if self.__view == 2 or self.__view == 3:
            if self.__view == 2:
                x = TermView.left_panel_end - 1
            else:
                x = TermView.left_panel_end + 18
            self.grid.add_block(x, self.ydim - 6,
                                "╤═════════════════════════════╤", BROWN)
            for by in range(4):
                self.grid.add_block(x, self.ydim - by - 2,
                                    "│                             │", BROWN)
            self.grid.add_block(x, self.ydim - 1,
                                "╧═════════════════════════════╧", BROWN)
            self.grid.add_block(x + 1, self.ydim - 5, RIGHT_PANEL, WHITE)
            if TermView.exit_found == 1:
                self.grid.add_block(x + 2, self.ydim - 3, "🪨", EXIT)

            txt = (f"{self.__width} x {self.__height} "
                   f"({self.__width * self.__height})")
            dx = x + 29 - len(txt)
            self.grid.add_block(dx, self.ydim - 5, txt, CYAN)
            ex, ey = self.__entry
            txt = f"{ex}, {ey}"
            dx = x + 29 - len(txt)
            self.grid.add_block(dx, self.ydim - 4, txt, CYAN)
            ex, ey = self.__exit
            txt = f"{ex}, {ey}"
            dx = x + 29 - len(txt)
            self.grid.add_block(dx, self.ydim - 3, txt, CYAN)
            txt = f"{self.__perfect}"
            dx = x + 29 - len(txt)
            self.grid.add_block(dx, self.ydim - 2, txt, CYAN)

        self.grid.print()

        while TermView.paused and not TermView.quit_requested:
            key = KEYS.poll()
            if key:
                TermView.handle_key(key)
            time.sleep(0.02)

        if self.__view != 3 or digger_xy is None:
            self.wait_for_quit()

    def display_genstep(self, x: int, y: int):
        if TermView.quit_requested:
            KEYS.exit_program()
        TermView.frame_count += 1
        self.display_maze((x, y))
        time.sleep(1 / TermView.speed)
