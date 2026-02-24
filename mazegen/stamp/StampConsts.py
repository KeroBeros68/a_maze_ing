"""Logo constants for maze stamping.

This module contains the ASCII art logos and stamp designs that can be
embedded into generated mazes.

Classes:
    FortyTwo: Collection of ASCII art logo designs
"""


class FortyTwo:
    """ASCII art logos for maze stamping.

    Contains multiple logo designs in different sizes for placement within
    the maze structure. Logos are represented as text blocks with specific
    characters marking locked cells.
    """
    VANILLA = [
        "        ",
        "        ",
        "F   FFF ",
        "F     F ",
        "FFF FFF ",
        "  F F   ",
        "  F FFF ",
        "        ",
    ]
    SMALL = [
        "Y",
    ]
    MEDIUM = [
        "         ",
        "         ",
        " F F FFF ",
        " F F   F ",
        " FFF FFF ",
        "   F F   ",
        "   F FFF ",
        "         ",
        "         ",
    ]
    MEDIUM_ALT = [
        "         ",
        "         ",
        " D R DFR ",
        " F F   F ",
        " LFF DFU ",
        "   F F   ",
        "   L LFU ",
        "         ",
        "         ",
    ]
    LARGE = [
        "                  ",
        "                  ",
        "                  ",
        "      DFFU FFUFFF ",
        "     DFFU  FU FFF ",
        "    DFFU   U  FFF ",
        "   DFFU      DFFU ",
        "  DFFU      DFFU  ",
        " DFFU      DFFU   ",
        " FFFFFFFFF FFF  D ",
        " FFFFFFFFF FFF DF ",
        " FFFFFFFFF FFFDFF ",
        "       FFF        ",
        "       FFF        ",
        "       FFF        ",
        "                  ",
        "                  ",
        "                  ",
    ]
