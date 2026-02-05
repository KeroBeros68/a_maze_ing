from random import randint
from mazegen.maze.maze import Maze
from mazegen.utils.utils import Direction, Wall


def backtrack(maze: Maze, x: int, y: int, nb_cell: int, nb_cell_max: int) -> Maze:
    if x == 0:
        limit_x = 0
    else:
        limit_x = -1
    if y == 0:
        limit_y = 0
    else:
        limit_y = -1

    if nb_cell == nb_cell_max:
        return maze

    maze.maze_grid[y][x].visit(True)
    x2 = x
    y2 = y
    while maze.maze_grid[y2][x2].visited is True:
        x2 = x + randint(limit_x, 1)
        y2 = y + randint(limit_y, 1)
    print("cellule actuel:", x, y)
    print("cellule voisine valide:", x2, y2)
    if x + 1 == x2:
        maze.maze_grid[y][x].remove_wall(Wall.EAST)
        maze.maze_grid[y2][x2].remove_wall(Direction.EAST.opposite.wall)
    maze = backtrack(maze, x2, y2, nb_cell + 1, nb_cell_max)
    return maze


if __name__ == "__main__":
    maze = Maze(10, 10, (0, 0), (9, 9))
    maze.init_grid()
    x, y = maze.entry
    maze = backtrack(maze, x, y, 0, 10 * 10)
    print(maze)
