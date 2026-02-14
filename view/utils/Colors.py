from enum import Enum


class ColorsTty(Enum):
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
    def get_ordered_colors(cls):
        """Retourne une liste ordonnée de couleurs spécifiques
        (excluant RESET, CLOSED, ENTRY, EXIT)."""
        excluded = {"RESET", "CLOSED", "ENTRY", "EXIT"}
        return [color for color in cls if color.name not in excluded]
