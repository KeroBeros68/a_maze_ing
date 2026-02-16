"""Abstract base class for maze visualization views.

This module defines the View abstract base class that all maze display
implementations must inherit from. It enforces the contract for rendering
mazes and changing display colors.

Classes:
    View: Abstract base class for maze visualization
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from mazegen.maze.maze import Maze
from view.utils.Colors import ColorsTty
from model import ConfigModel


class View(ABC):
    """Abstract base class for maze visualization.

    Defines the interface that all maze visualization implementations must
    follow, including rendering the maze and color customization.

    Attributes:
        __color: Current color setting for the display
    """

    def __init__(self, config: ConfigModel) -> None:
        """Initialize the view with default colors settings."""
        self.__color_list: Optional[List[ColorsTty]] = None
        self.__active_color: Optional[ColorsTty] = None
        self.__entry_color: Optional[ColorsTty] = None
        self.__exit_color: Optional[ColorsTty] = None
        self.__closed_color: Optional[ColorsTty] = None
        self.__config: ConfigModel = config

    @abstractmethod
    def render(self, maze: Maze, speed: int, count_as_step: Optional[int] = 1) -> None:
        """Render the maze to the display.

        Args:
            maze: The Maze object to render
            speed: Animation speed in frames per second
        """
        pass

    @abstractmethod
    def change_color(self, new_color: int) -> None:
        """Change the display color.

        Args:
            new_color: The new color value to apply
        """
        pass
