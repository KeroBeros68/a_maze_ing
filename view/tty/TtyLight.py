from view.tty.TtyView import TtyView
from view.tty.TtyUtils import Canvas
from mazegen.maze.maze import Maze
from typing import Tuple
import heapq


class Light:
    def __init__(self, view: TtyView, grid: Canvas, maze: Maze) -> None:
        self.view = view
        self.grid = grid
        self.__maze = maze
        self.width = self.grid.width
        self.height = self.grid.height
        self.xoffset = self.view.xoffset
        self.yoffset = self.view.yoffset

    def reset_light_zone(self, x1: int, y1: int, x2: int, y2: int) -> None:
        ansi_off: str = str(self.grid.color_wall_ground(0))
        for y in range(y1, y2):
            for x in range(x1, x2):
                x_cell = int((x - self.xoffset) / 6)
                y_cell = int((y - self.yoffset) / 3)
                cell = self.__maze.maze_grid[y_cell][x_cell]
                if cell.view_cell() == "F" or cell.locked is True:
                    continue
                self.grid._grid[y][x].color = ansi_off
                self.grid._grid[y][x].lit = 0

    def light_cell_from_xy(self, x: int, y: int, lit: float) -> None:
        x_cell = int((x - self.xoffset) / 6)
        y_cell = int((y - self.yoffset) / 3)
        self.light_cell(x=x_cell, y=y_cell, lit_max=lit, dim_lit=1 / (2 * lit))

    def light_cell(
        self,
        x: int,
        y: int,
        *,
        lit_max: float = 2.0,
        dim_lit: float = 0.25,
        turn_cost: float = 0.25,
    ) -> None:

        def cell_code(mx: int, my: int) -> int:
            return int(str(maze.maze_grid[my][mx].view_cell()), 16)

        def locked(mx: int, my: int) -> bool:
            return bool(maze.maze_grid[my][mx].locked)

        def square_to_canvas(sx: int, sy: int) -> Tuple[int, int]:
            cx = self.xoffset + (sx * 2)
            cy = self.yoffset + sy
            return cx, cy

        def square_to_maze(sx: int, sy: int) -> Tuple[int, int, int, int]:
            mx = sx // 3
            my = sy // 3
            lsx = sx % 3
            lsy = sy % 3
            return mx, my, lsx, lsy

        def can_step(sx: int, sy: int, nsx: int, nsy: int) -> bool:
            if not (0 <= nsx < sw and 0 <= nsy < sh):
                return False

            mx, my, lsx, lsy = square_to_maze(sx, sy)
            nmx, nmy, nlsx, nlsy = square_to_maze(nsx, nsy)

            if locked(nmx, nmy):
                return False

            if mx == nmx and my == nmy:
                return True

            code = cell_code(mx, my)

            if nmx == mx and nmy == my - 1:
                return (code & 1) == 0
            if nmx == mx and nmy == my + 1:
                return (code & 4) == 0
            if nmx == mx + 1 and nmy == my:
                return (code & 2) == 0
            if nmx == mx - 1 and nmy == my:
                return (code & 8) == 0

            return False

        def ansi_for(lit: float) -> str:
            lit = max(0.0, min(lit_max, lit))
            dr, dg, db, dgr, dgg, dgb = self.grid.color_wall_ground_raw(lit)
            return f"\33[38;2;{dr};{dg};{db}m\33[48;2;{dgr};{dgg};{dgb}m"

        def write_square(sx: int, sy: int, lit: float) -> None:
            if lit <= 0.0:
                return
            cx, cy = square_to_canvas(sx, sy)

            if not (0 <= cy < self.height and 0 <= cx < self.width - 1):
                return

            cur0 = self.grid._grid[cy][cx].lit
            cur1 = self.grid._grid[cy][cx + 1].lit
            if cur0 > lit and cur1 > lit:
                return

            color = ansi_for(lit)
            self.grid._grid[cy][cx].lit = lit
            self.grid._grid[cy][cx + 1].lit = lit
            self.grid._grid[cy][cx].color = color
            self.grid._grid[cy][cx + 1].color = color

        maze = self.__maze
        mw, mh = maze.width, maze.height
        if not (0 <= x < mw and 0 <= y < mh):
            return
        if maze.maze_grid[y][x].locked:
            return
        if lit_max <= 0:
            return
        dim_lit = max(0.0001, float(dim_lit))
        turn_cost = max(0.0, float(turn_cost))

        sw = mw * 3
        sh = mh * 3
        src_sx = x * 3 + 1
        src_sy = y * 3 + 1
        best = [[[0.0, 0.0, 0.0, 0.0] for _ in range(sw)] for __ in range(sh)]

        heap: list[tuple[float, int, int, int]] = []
        for oy in (-1, 0, 1):
            for ox in (-1, 0, 1):
                sx0 = src_sx + ox
                sy0 = src_sy + oy
                if ox*ox + oy*oy <= 2:
                    mx0 = sx0 // 3
                    my0 = sy0 // 3
                    if maze.maze_grid[my0][mx0].locked:
                        continue
                    heapq.heappush(heap, (-lit_max, sx0, sy0, -1))
                    for d in range(4):
                        best[sy0][sx0][d] = lit_max
        while heap:
            neg_lit, sx, sy, pdir = heapq.heappop(heap)
            lit = -neg_lit
            if lit <= 0.0:
                continue
            if pdir != -1 and lit < best[sy][sx][pdir]:
                continue

            write_square(sx, sy, lit)

            for ndr, (dx, dy) in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
                nsx, nsy = sx + dx, sy + dy
                if not can_step(sx, sy, nsx, nsy):
                    continue

                cost = dim_lit
                if pdir != -1 and ndr != pdir:
                    cost += turn_cost

                nl = lit - cost
                if nl <= 0.0:
                    continue

                if nl <= best[nsy][nsx][ndr]:
                    continue
                best[nsy][nsx][ndr] = nl
                heapq.heappush(heap, (-nl, nsx, nsy, ndr))
