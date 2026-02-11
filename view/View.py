from abc import ABC, abstractmethod

from mazegen.maze.maze import Maze


class View(ABC):
    def __init__(self):
        self.__color = None

    @abstractmethod
    def render(self, maze: Maze) -> None:
        pass

    def change_color(self, new_color) -> None:
        self.__color = new_color
