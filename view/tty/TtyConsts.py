"""TTY display constants and assets for maze visualization.

This module contains all display constants for the TTY (teletypewriter) view,
including color codes, banner art, UI panels, and animation elements.

Classes:
    Colors: ANSI color codes with RGB background
    Banners: ASCII art banners and signatures
    Panels: UI panel text and content
    Elements: Animation and display elements
"""


class Colors:
    """ANSI color codes for TTY display with black background.

    Defines color constants used in TTY view with RGB background set to black
    for consistent maze visualization.
    """
    RED = "\33[31m\33[48;2;0;0;0m"
    GREEN = "\33[32m\33[48;2;0;0;0m"
    BROWN = "\33[33m\33[48;2;0;0;0m"
    PURPLE = "\33[35m\33[48;2;0;0;0m"
    CYAN = "\33[36m\33[48;2;0;0;0m"
    WHITE = "\33[37m\33[48;2;0;0;0m"
    BLUE42 = "\33[38;2;16;32;96m\33[48;2;0;0;0m"
    DEEP_PURPLE = "\33[38;2;54;18;72m\33[48;2;0;0;0m"
    DEEP_BROWN = "\33[38;2;60;45;30m\33[48;2;0;0;0m"
    DARK_BROWN = "\33[38;2;30;22;15m\33[48;2;0;0;0m"
    CLOSED = "\33[38;2;32;16;8m\33[48;2;0;0;0m"
    ENTRY = "\33[38;5;45m\33[48;2;0;0;0m"
    EXIT = "\33[38;5;208m\33[48;2;0;0;0m"

    RESET = "\33[0;1;37m\33[48;2;0;0;0m"


class Banners:
    LEFT_BANNER = [
        " ◢◤ ◤█",
        "◢◤  ◢◤",
        "███ █◢",
        "  █   ",
        " 2026 ",
        "      ",
        "      ",
        " OPR  ",
    ]
    RIGHT_BANNER = [
        "█◥ ◥◣ ",
        "◥◣  ◥◣",
        "◣█ ███",
        "   █  ",
        " 2026 ",
        "      ",
        "      ",
        " Kero ",
    ]
    CENTER_BANNER = [
        "     ▁▁▁           ▁▁  ▁▁▁                         ▁▁            ",
        "    ╱   │         ╱  │╱  ╱▁▁▁▁▁▁▁▁▁  ▁▁▁          ╱▁╱▁▁▁  ▁▁▁▁▁▁ ",
        "   ╱ ╱│ │ ▁▁▁▁▁▁ ╱ ╱│▁╱ ╱ ▁▁  ╱▁  ╱ ╱ ▁ ╲ ▁▁▁▁▁▁ ╱ ╱ ▁▁ ╲╱ ▁▁  ╱ ",
        "  ╱ ▁▁▁ │╱▁▁▁▁▁╱╱ ╱  ╱ ╱ ╱▁╱ ╱ ╱ ╱▁╱  ▁▁╱╱▁▁▁▁▁╱╱ ╱ ╱ ╱ ╱ ╱▁╱ ╱  ",
        " ╱▁╱  │▁│      ╱▁╱  ╱▁╱╲▁▁▁▁╱ ╱▁▁▁╱╲▁▁▁╱       ╱▁╱▁╱ ╱▁╱╲▁▁  ╱   ",
        "                                                       ╱▁▁▁▁╱    ",
    ]
    SIGNATURE_BANNER = "   42 - orobert & kebertra - 2026"
    SIGNATURE_COLORS = "000660305555555030555555550306666"


class Panels:
    ANIM_LEFT_PANEL = [
        " Space/P : Pause            ",
        " +/-     : Speed            ",
        " C/V     : Color            ",
        " R       : Recreate Maze    ",
        " E       : Regenerate Seed  ",
        " ESC     : Exit             ",
    ]
    LEFT_PANEL = [
        " F       : Show/Hide Path   ",
        " G       : Game on, Garth!  ",
        " C/V     : Color            ",
        " R       : Regen same Maze  ",
        " E       : Regen Seed+Maze  ",
        " ESC     : Exit             ",
    ]
    GAME_PANEL = [
        " W/A/S/D : Movement         ",
        " G       : Back to Serious  ",
        " C/V     : Color            ",
        " R       : Regen same Maze  ",
        " E       : Regen Seed+Maze  ",
        " ESC     : Exit             ",
    ]
    RIGHT_PANEL = [
        " Size    :                  ",
        " 🚪Entry :                  ",
        "   Exit  :                  ",
        " Perfect :                  ",
        " Seed    :                  ",
        "                            ",
    ]
    VERT_BAR = [
        "╤",
        "│",
        "│",
        "│",
        "│",
        "│",
        "│",
        "╧",
    ]


class Elements:
    LARGE_DIGITS = [
        "┏━┓╺┓ ┏━┓┏━┓╻ ╻┏━╸┏━┓┏━┓┏━┓┏━┓",
        "┃ ┃ ┃ ┏━┛ ╺┫┗━┫┗━┓┣━┓  ┃┣━┫┗━┫",
        "┗━┛╺┻╸┗━╸┗━┛  ╹┗━┛┗━┛  ╹┗━┛┗━┛",
    ]
    CLOSED_CELL = [
        "▒▒▒▒▒▒",
        "▒▒░░▒▒",
        "▒▒▒▒▒▒",
    ]
    BLANK_CELL = [
        "      ",
        "      ",
        "      ",
    ]
    DECO_FILL = [
        "──┘ │ ├─",
        "┌─┐ ╵ │ ",
        "╵ ├─╴ ╵ ",
        "╴ │ ┌─┬─",
    ]
    TATADATAAA = [
        "╺┳╸┏━┓🎶╺┳╸┏━┓╺┳┓┏━┓",
        " ┃ ┣━┫ ━ ┃ ┣━┫ ┃┃┣━┫",
        " ╹ ╹ ╹   ╹ ╹ ╹╺┻┛╹ ╹",
        " 🎵╺┳╸┏━┓┏━┓┏━┓ ╻ 🎶",
        "🎶  ┃ ┣━┫┣━┫┣━┫ ╹   ",
        "    ╹ ╹ ╹╹ ╹╹ ╹ ╹🎵 ",
    ]


class FortyTwoBrick:
    Y = [
        "╻ ╻┏━┓",
        "┗━┫┏━┛",
        "  ╹┗━╸",
    ]
    F = [
        "██████",
        "██████",
        "██████",
    ]
    E = [
        "      ",
        "      ",
        "      ",
    ]
    D = [
        "    ▄█",
        "  ▄███",
        "▄█████",
    ]
    U = [
        "█████▀",
        "███▀  ",
        "█▀    ",
    ]
    R = [
        "█▄    ",
        "███▄  ",
        "█████▄",
    ]
    L = [
        "▀█████",
        "  ▀███",
        "    ▀█",
    ]


class Endgame:
    FRAME = [
        "╔════════════════════════════════════════════════════════════════════════╗",  # noqa E501
        "║                                              Your moves    :           ║",  # noqa E501
        "║                                              Shortest path :           ║",  # noqa E501
        "║                                              Efficiency    :           ║",  # noqa E501
        "║   [R] Retry same maze   [E] Create new maze    [G] Back   [ESC] Quit   ║",  # noqa E501
        "╚════════════════════════════════════════════════════════════════════════╝",  # noqa E501
    ]
    TEXT = [
        "                                              Your moves    :           ",  # noqa E501
        "                                              Shortest path :           ",  # noqa E501
        "                                              Efficiency    :           ",  # noqa E501
        "   [R] Retry same maze   [E] Create new maze    [G] Back   [ESC] Quit   ",  # noqa E501
    ]
    BUTTONS = [
        "    R                     E                      G          ESC         ",  # noqa E501
    ]
    AMAZING = [
        "            ┏━┓┏┳┓┏━┓╺━┓╻┏┓╻┏━╸  ╻            ",
        "            ┣━┫┃┃┃┣━┫┏━┛┃┃┗┫┃╺┓  ╹            ",
        "            ╹ ╹╹ ╹╹ ╹┗━╸╹╹ ╹┗━┛  ╹            ",
    ]
    WELL_DONE = [
        "         ╻ ╻┏━╸╻  ╻   ╺┳┓┏━┓┏┓╻┏━╸  ╻         ",
        "         ┃╻┃┣╸ ┃  ┃    ┃┃┃ ┃┃┗┫┣╸   ╹         ",
        "         ┗┻┛┗━╸┗━╸┗━╸ ╺┻┛┗━┛╹ ╹┗━╸  ╹         ",
    ]
    NOT_BAD = [
        "             ┏┓╻┏━┓╺┳╸  ┏┓ ┏━┓╺┳┓             ",
        "             ┃┗┫┃ ┃ ┃   ┣┻┓┣━┫ ┃┃             ",
        "             ╹ ╹┗━┛ ╹   ┗━┛╹ ╹╺┻┛             ",
    ]
    LOST = [
        "  ╻ ╻┏━╸┏━┓┏━╸  ╻ ╻┏━┓╻ ╻  ╻  ┏━┓┏━┓╺┳╸  ┏━┓  ",
        "  ┃╻┃┣╸ ┣┳┛┣╸   ┗┳┛┃ ┃┃ ┃  ┃  ┃ ┃┗━┓ ┃    ╺┛  ",
        "  ┗┻┛┗━╸╹┗╸┗━╸   ╹ ┗━┛┗━┛  ┗━╸┗━┛┗━┛ ╹    ╹   ",
    ]
