from dataclasses import dataclass
from typing import List, Iterable
import unicodedata
import sys
from view.tty.TtyConsts import Colors, Banners, Elements, FortyTwoBrick


@dataclass(slots=True)
class CanvasCell:
    ch: str = " "
    color: str = ""
    cont: bool = False


class Canvas:
    def __init__(
            self,
            width: int,
            height: int,
            color_theme: int,
            default: CanvasCell | None = None
            ) -> None:
        self.width = width
        self.height = height
        self.color_theme = color_theme
        self.color_wall_ground(0)
        base = default if default is not None else CanvasCell(" ", "")
        self._grid: List[List[CanvasCell]] = [
            [CanvasCell(base.ch, base.color) for _ in range(width)]
            for _ in range(height)
        ]
        self._prev_lines: list[str] | None = None

    @staticmethod
    def utfchar_len(s: str) -> int:
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

    def set_canvas_cell(self, x: int, y: int, ch: str,
                        color: str = "") -> None:
        self._grid[y][x].ch = ch
        self._grid[y][x].color = color
        self._grid[y][x].cont = False
        char_width = self.utfchar_len(ch)
        if char_width == 2 and x + 1 < self.width:
            self._grid[y][x + 1].ch = ""
            self._grid[y][x + 1].color = ""
            self._grid[y][x + 1].cont = True

    def color_canvas_cell(self, x: int, y: int, color: str = "") -> None:
        self._grid[y][x].color = color

    def color_canvas_block(self, x1: int, y1: int, x2: int, y2: int,
                           color: str = "") -> None:
        for dy in range(y2 - y1 + 1):
            for dx in range(x2 - x1 + 1):
                self.color_canvas_cell(x1 + dx, y1 + dy, color)

    def get_canvas_cell(self, x: int, y: int) -> CanvasCell:
        return self._grid[y][x]

    def clear_canvas(self, ch: str = " ", color: str = "") -> None:
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
        block_width, block_height = self.measure_block(block)
        xs = max(0, min(self.width, x_start))
        xe = max(0, min(self.width, x_end))
        ys = max(0, min(self.height, y_start))
        ye = max(0, min(self.height, y_end))
        if xe < xs:
            xs, xe = xe, xs
        if ye < ys:
            ys, ye = ye, ys
        zone_width = max(0, xe - xs)
        zone_height = max(0, ye - ys)
        x = xs + (zone_width - block_width) // 2 + offset_x
        y = ys + (zone_height - block_height) // 2 + offset_y
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
        src_w = max((len(line) for line in src_lines), default=0)
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
                char_width = self.utfchar_len(ch)
                if char_width == 0:
                    continue
                if transparent and ch in transparent_chars:
                    gx += char_width
                    if gx >= self.width:
                        break
                    continue
                if 0 <= gx < self.width:
                    self.set_canvas_cell(gx, gy, ch, color)
                gx += char_width
                if gx >= self.width:
                    break

    def add_maze_locked_cell(self, x: int, y: int, lock_code: str) -> None:
        ansi = self.color_wall_ground(0, bright=True)
        if lock_code == "Y":
            self.add_block(x, y, FortyTwoBrick.Y, ansi)
        elif lock_code == "F":
            self.add_block(x, y, FortyTwoBrick.F, ansi)
        elif lock_code == "E":
            self.add_block(x, y, FortyTwoBrick.E, ansi)
        elif lock_code == "U":
            self.add_block(x, y, FortyTwoBrick.U, ansi)
        elif lock_code == "D":
            self.add_block(x, y, FortyTwoBrick.D, ansi)
        elif lock_code == "L":
            self.add_block(x, y, FortyTwoBrick.L, ansi)
        elif lock_code == "R":
            self.add_block(x, y, FortyTwoBrick.R, ansi)

    def add_maze_cell(self, x: int, y: int, cell: str) -> None:
        code = int(cell, 16)
        ansi = self.color_wall_ground(0)
        ansi_closed = self.color_wall_ground(-1)
        if code == 15:
            self.add_block(x, y, Elements.CLOSED_CELL, ansi_closed)
            return
        self.add_block(x, y, Elements.BLANK_CELL, ansi)
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

    def color_wall_ground(self, lit: int, inv: bool = False,
                          bright: bool = False) -> str:
        r, g, b = 96, 48, 24
        if self.color_theme == 1:
            r, g, b = 96, 48, 24
            self.color_theme_name = "Cave"
        elif self.color_theme == 2:
            r, g, b = 16, 64, 32
            self.color_theme_name = "Forest"
        elif self.color_theme == 3:
            r, g, b = 16, 32, 96
            self.color_theme_name = "DeepBlue"
        elif self.color_theme == 4:
            r, g, b = 55, 0, 54
            self.color_theme_name = "WitchLace"
        elif self.color_theme == 5:
            r, g, b = 96, 4, 8
            self.color_theme_name = "Volcano"
        elif self.color_theme == 6:
            r, g, b = 128, 64, 96
            self.color_theme_name = "CandyShop"
        elif self.color_theme == 7:
            r, g, b = 64, 32, 128
            self.color_theme_name = "Fluffy"
        elif self.color_theme == 8:
            r, g, b = 0, 91, 118
            self.color_theme_name = "Smurfy"
        dr = int(r + ((r / 2) * lit))
        dg = int(g + ((g / 2) * lit))
        db = int(b + ((b / 2) * lit))
        dr = max(0, min(255, dr))
        dg = max(0, min(255, dg))
        db = max(0, min(255, db))
        gr = "\33[48;2;0;0;0m"
        if lit == 1:
            gr = "\33[48;2;16;16;16m"
        if lit == 2:
            gr = "\33[48;2;32;32;32m"
        if lit == 4:
            gr = "\33[48;2;64;64;64m"
        if inv is True:
            ansi = f"\33[38;2;0;0;0m\33[48;2;{dr};{dg};{db}m"
        if bright is True:
            br = min(255, dr * 2)
            bg = min(255, dg * 2)
            bb = min(255, db * 2)
            ansi = f"\33[38;2;{br};{bg};{bb}m\33[48;2;{dr};{dg};{db}m"
        else:
            ansi = f"\33[38;2;{dr};{dg};{db}m{gr}"
        return ansi

    def render_canvas(self, reset_each_cell: bool = False) -> str:
        lines: List[str] = []
        rows_in_line: List[str] = []
        if reset_each_cell:
            for y in range(self.height):
                rows_in_line = []
                for x in range(self.width):
                    cell = self._grid[y][x]
                    if cell.cont:
                        continue
                    if cell.color:
                        rows_in_line.append(cell.color)
                        rows_in_line.append(cell.ch)
                        rows_in_line.append(Colors.RESET)
                    else:
                        rows_in_line.append(cell.ch)
                lines.append("".join(rows_in_line) + Colors.RESET)
            return "\n".join(lines)

        for y in range(self.height):
            current_color = ""
            rows_in_line = []
            for x in range(self.width):
                cell = self._grid[y][x]
                if cell.cont:
                    continue
                c = cell.color
                if c and c != current_color:
                    rows_in_line.append(c)
                    current_color = c
                elif not c and current_color:
                    rows_in_line.append(Colors.RESET)
                    current_color = ""
                rows_in_line.append(cell.ch)
            if current_color:
                rows_in_line.append(Colors.RESET)
            lines.append("".join(rows_in_line))
        return "\n".join(lines)

    def print_canvas(self) -> None:
        canvas = self.render_canvas()
        new_lines = canvas.splitlines()

        if self._prev_lines is None:
            sys.stdout.write("\33[H\33[2J\33[?25l\33[1m\n")
            sys.stdout.write(canvas)
            sys.stdout.flush()
            self._prev_lines = new_lines
            return

        prev = self._prev_lines
        if len(new_lines) != len(prev):
            sys.stdout.write("\33[H\33[2J\33[?25l\33[1m\n")
            sys.stdout.write(canvas)
            sys.stdout.flush()
            self._prev_lines = new_lines
            return

        changed: list[int] = []
        for i, line in enumerate(new_lines):
            if line != prev[i]:
                changed.append(i)

        if not changed:
            return

        out: list[str] = []
        out.append("\33[?25l\33[1m")

        base_row = 2

        first = changed[0]
        last = changed[0]
        for idx in changed[1:] + [None]:
            if idx is not None and idx == last + 1:
                last = idx
                continue

            out.append(f"\33[{base_row + first};1H")
            out.append("\n".join(new_lines[first:last + 1]))
            out.append("\33[K")

            prev[first:last + 1] = new_lines[first:last + 1]

            if idx is None:
                break
            first = last = idx

        sys.stdout.write("".join(out))
        sys.stdout.write(f"\33[H\33[{self.height + 1};1H")
        sys.stdout.flush()

    def template(self) -> None:
        for x in range(self.width):
            if x > 0:
                self.set_canvas_cell(x, 0, "═", Colors.BROWN)
                self.set_canvas_cell(x, 9, "═", Colors.BROWN)
                self.set_canvas_cell(x, self.height - 8, "═", Colors.BROWN)
                self.set_canvas_cell(x, self.height - 1, "═", Colors.BROWN)
        for y in range(self.height):
            self.set_canvas_cell(1, y, "║", Colors.BROWN)
            self.set_canvas_cell(self.width - 1, y, "║", Colors.BROWN)
        self.set_canvas_cell(1, 0, "╔", Colors.BROWN)
        self.set_canvas_cell(self.width - 1, 0, "╗", Colors.BROWN)
        self.set_canvas_cell(1, self.height - 1, "╚", Colors.BROWN)
        self.set_canvas_cell(self.width - 1, self.height - 1, "╝",
                             Colors.BROWN)
        self.set_canvas_cell(1, 9, "╠", Colors.BROWN)
        self.set_canvas_cell(1, self.height - 8, "╠", Colors.BROWN)
        self.set_canvas_cell(self.width - 1, 9, "╣", Colors.BROWN)
        self.set_canvas_cell(self.width - 1, self.height - 8, "╣",
                             Colors.BROWN)
        self.deco_zone(2, 1, self.width - 2, 8, Elements.DECO_FILL,
                       Colors.DEEP_PURPLE)
        self.add_block(2, 1, Banners.LEFT_BANNER, Colors.BLUE42,
                       transparent=True)
        self.add_block(self.width - 7, 1, Banners.RIGHT_BANNER, Colors.BLUE42,
                       transparent=True)
        x, y = self.center_block(Banners.CENTER_BANNER,
                                 x_start=8, x_end=self.width - 7)
        self.add_block(x, 1, Banners.CENTER_BANNER, Colors.PURPLE,
                       transparent=True)
        bx, by = self.measure_block(Banners.CENTER_BANNER)
        x, y = self.center_block(Banners.SIGNATURE_BANNER,
                                 x_start=8, x_end=self.width - 7)
        self.add_block(x, 8, Banners.SIGNATURE_BANNER, Colors.BROWN,
                       transparent=True)
        for i in range(len(Banners.SIGNATURE_COLORS)):
            if Banners.SIGNATURE_COLORS[i] != "0":
                color = f"\33[3{Banners.SIGNATURE_COLORS[i]}m"
                self.color_canvas_cell(x + i, 8, color)
        self.deco_zone(2, 10, self.width - 2, self.height - 9,
                       Elements.DECO_FILL, Colors.DARK_BROWN)

    def large_counter_block(
        self,
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
                block_lines[0] += Elements.LARGE_DIGITS[0][start:end]
                block_lines[1] += Elements.LARGE_DIGITS[1][start:end]
                block_lines[2] += Elements.LARGE_DIGITS[2][start:end]
            else:
                block_lines[0] += " " * 3
                block_lines[1] += " " * 3
                block_lines[2] += " " * 3
        return "\n".join(block_lines)
