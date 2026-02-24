from collections import deque
from typing import Deque, Dict, Optional, Tuple
from mazegen.maze.maze import Maze


class PathFinder:
    """Solver for finding the shortest path through a maze.

    Uses a Breadth-First Search (BFS) algorithm to find the shortest
    path from the maze entry to its exit, then stores the result as
    a sequence of cardinal directions (N, E, S, W) in the maze.
    """

    def solve_shortest_path(self, maze: Maze) -> None:
        """Find and store the shortest path from entry to exit.

        Runs BFS from maze.entry to maze.exit, reconstructing the path
        by backtracking through visited nodes. The result is stored as
        a string of directions (N/E/S/W) in maze.shortest_path.
        Locked cells (stamp pattern) are treated as impassable.

        Args:
            maze: The Maze instance to solve. Must have entry and exit set.

        Returns:
            None. Result is written directly to maze.shortest_path.
        """
        start = maze.entry
        goal = maze.exit

        prev: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}
        q: Deque[Tuple[int, int]] = deque()
        q.append(start)
        visited = set([start])

        def can_go(x: int, y: int, nx: int, ny: int) -> Optional[str]:
            if not (0 <= nx < maze.width and 0 <= ny < maze.height):
                return None
            if maze.maze_grid[ny][nx].locked:
                return None

            cell = maze.maze_grid[y][x]
            code = int(f"{cell.view_cell()}", 16)
            dx = nx - x
            dy = ny - y

            if dx == 0 and dy == -1:
                return None if code & 1 else "N"
            if dx == 1 and dy == 0:
                return None if code & 2 else "E"
            if dx == 0 and dy == 1:
                return None if code & 4 else "S"
            if dx == -1 and dy == 0:
                return None if code & 8 else "W"
            return None

        while q:
            x, y = q.popleft()
            if (x, y) == goal:
                break
            for nx, ny in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)):
                if (nx, ny) in visited:
                    continue
                step = can_go(x, y, nx, ny)
                if step is None:
                    continue
                visited.add((nx, ny))
                prev[(nx, ny)] = ((x, y), step)
                q.append((nx, ny))

        if goal not in visited:
            return

        moves = []
        cur = goal
        while cur != start:
            p, move = prev[cur]
            moves.append(move)
            cur = p

        moves.reverse()
        maze.shortest_path = "".join(moves)
