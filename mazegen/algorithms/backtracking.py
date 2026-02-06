"""Backtracking maze generation algorithm.

This module implements the depth-first search backtracking algorithm
for generating perfect mazes. It carves passages by removing walls
between adjacent unvisited cells.
"""

import random
from typing import Tuple
from mazegen.maze.maze import Maze
from mazegen.utils.utils import Direction, Wall


def backtrack(maze: Maze, x: int, y: int) -> Maze:
    """Generate a maze using the backtracking algorithm.

    Uses depth-first search with a stack to carve passages through the maze.
    Starting from entry coordinates, recursively visits unvisited neighbors
    and removes walls between visited and current cells.

    Args:
        maze: Maze object to generate
        x: Starting X coordinate
        y: Starting Y coordinate

    Returns:
        Maze: The modified maze with passages carved by the algorithm
    """
    stack = [(x, y)]

    while stack:
        x1, y1 = stack[len(stack) - 1]
        maze.maze_grid[y1][x1].visit(True)
        try:
            target = valid_target(x1, y1, maze)
            x2, y2 = target
            maze = remove_wall(x1, y1, x2, y2, maze)
            x1, y1 = x2, y2
            stack.append((x1, y1))
        except Exception:
            stack.pop()
    return maze


def valid_target(x: int, y: int, maze: Maze) -> Tuple[int, int]:
    """Find a random unvisited neighbor of the current cell.

    Checks all four adjacent cells (North, South, East, West) and
    returns a random choice from unvisited neighbors that are within
    maze bounds.

    Args:
        x: Current cell X coordinate
        y: Current cell Y coordinate
        maze: Maze object containing grid and dimensions

    Returns:
        Tuple[int, int]: Coordinates (x, y) of a random valid target cell

    Raises:
        IndexError: If no valid targets are available (all neighbors visited)
    """
    target = [
        (x + dx, y + dy)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ]

    valid_target = [
        (vx, vy) for vx, vy in target
        if 0 <= vx < maze.width and 0 <= vy < maze.height
        and not maze.maze_grid[vy][vx].visited
    ]

    return random.choice(valid_target)


def remove_wall(x: int, y: int, x1: int, y1: int, maze: Maze) -> Maze:
    """Remove walls between two adjacent cells to create a passage.

    Determines the direction from current cell to target cell and removes
    the corresponding wall from both cells. This creates a passage between
    the two cells.

    Args:
        x: Current cell X coordinate
        y: Current cell Y coordinate
        x1: Target cell X coordinate
        y1: Target cell Y coordinate
        maze: Maze object containing the grid to modify

    Returns:
        Maze: The modified maze with walls removed
    """
    if x + 1 == x1:
        maze.maze_grid[y][x].remove_wall(Wall.EAST)
        maze.maze_grid[y1][x1].remove_wall(Direction.EAST.opposite.wall)
    if x - 1 == x1:
        maze.maze_grid[y][x].remove_wall(Wall.WEST)
        maze.maze_grid[y1][x1].remove_wall(Direction.WEST.opposite.wall)
    if y + 1 == y1:
        maze.maze_grid[y][x].remove_wall(Wall.SOUTH)
        maze.maze_grid[y1][x1].remove_wall(Direction.SOUTH.opposite.wall)
    if y - 1 == y1:
        maze.maze_grid[y][x].remove_wall(Wall.NORTH)
        maze.maze_grid[y1][x1].remove_wall(Direction.NORTH.opposite.wall)
    return maze


if __name__ == "__main__":
    maze = Maze(10, 10, (5, 0), (9, 9))
    maze.init_grid()
    x, y = maze.entry
    random.seed(42)
    maze = backtrack(maze, x, y)
    print(maze)
