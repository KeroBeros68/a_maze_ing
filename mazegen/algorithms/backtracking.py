import random
from typing import Tuple
from mazegen.maze.maze import Maze
from mazegen.utils.utils import Direction, Wall


def backtrack(maze: Maze, x: int, y: int, nb_cell: int,
              nb_cell_max: int) -> Maze:
    stack = [(x, y)]

    while stack:
        x1, y1 = stack[len(stack) - 1]
        maze.maze_grid[y1][x1].visit(True)
        print(x1, y1)
        try:
            target = valid_target(x1, y1, maze)
            x2, y2 = target
            maze = remove_wall(x1, y1, x2, y2, maze)
            x1, y1 = x2, y2
            stack.append((x1, y1))
        except Exception as e:
            print(e)
            stack.pop()
    return maze


def valid_target(x: int, y: int, maze: Maze) -> Tuple[int, int]:
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


def remove_wall(x, y, x1, y1, maze: Maze):
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
    maze = Maze(10, 10, (0, 0), (9, 9))
    maze.init_grid()
    x, y = maze.entry
    maze = backtrack(maze, x, y, 0, 10 * 10)
    print(maze)
