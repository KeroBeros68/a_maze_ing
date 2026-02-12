from abc import ABC, abstractmethod

from mazegen.maze.maze import Maze


class View(ABC):
    def __init__(self) -> None:
        self.__color = 1

    @abstractmethod
    def render(self, maze: Maze, speed: int) -> None:
        pass

    @abstractmethod
    def change_color(self, new_color: int) -> None:
        pass
