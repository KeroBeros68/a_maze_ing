"""ANSI color codes for terminal display.

This module defines TTY color constants using ANSI escape sequences for
terminal-based maze visualization with various color themes.

Classes:
    ColorsTty: Enumeration of ANSI color codes
"""

from enum import Enum


class ColorsTty(Enum):
    """ANSI color codes for terminal display.

    Defines various TTY colors using ANSI escape sequences. Special colors
    include ENTRY (maze entry point), EXIT (maze exit point), and CLOSED
    (visited cells).

    Attributes:
        BLACK, RED, GREEN, BROWN, PURPLE, CYAN, WHITE: Standard colors
        BLUE42, DEEP_PURPLE, DEEP_BROWN: Custom RGB colors
        CLOSED: Color for visited cells
        ENTRY: Color for maze entry point
        EXIT: Color for maze exit point
        RESET: Reset formatting to default
    """

    BLACK = "\33[30m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    BROWN = "\33[33m"
    PURPLE = "\33[35m"
    CYAN = "\33[36m"
    WHITE = "\33[37m"
    BLUE42 = "\33[38;2;16;32;96m"
    DEEP_PURPLE = "\33[38;2;54;18;72m"
    DEEP_BROWN = "\33[38;2;60;45;30m"
    CLOSED = "\33[38;2;32;16;8m"
    ENTRY = "\33[38;5;45m"
    EXIT = "\33[38;5;208m"

    RESET = "\33[0;1;37m"

    @classmethod
    def get_ordered_colors(cls) -> list:
        """Get an ordered list of maze display colors.

        Returns all color values except RESET, CLOSED, ENTRY, and EXIT
        which are reserved for special purposes.

        Returns:
            list: Ordered list of ColorsTty values for maze rendering
        """
        excluded = {"RESET", "CLOSED", "ENTRY", "EXIT"}
        return [color for color in cls if color.name not in excluded]
