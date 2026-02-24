"""Maze error hierarchy.

This module defines the base exception class for the mazegen package
and its specialized child classes.
"""


class MazeError(Exception):
    """Base exception class for all mazegen errors.

    All exceptions raised by the mazegen package should inherit from
    this class to allow callers to catch them with a single handler.
    """

    def __init__(self, message: str = "An error occurred in the maze."):
        super().__init__(message)


class StampError(MazeError):
    """Exception raised for errors related to maze stamps.

    Raised when a stamp operation fails, e.g. invalid stamp dimensions,
    unsupported stamp format, or a stamp that does not fit in the maze.
    """

    def __init__(self, message: str = "An error occurred with the stamp."):
        super().__init__(message)
