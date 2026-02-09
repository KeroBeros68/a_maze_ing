"""Utility enumerations for maze wall and direction representation.

This module provides enums for representing walls as bit flags and
directions with their corresponding opposite directions.
"""

from enum import IntEnum, Enum


class Wall(IntEnum):
    """Four directional walls represented as bit flags.

    Each wall is a single bit in a 4-bit representation:
    - NORTH: 0x1 (0001)
    - EAST:  0x2 (0010)
    - SOUTH: 0x4 (0100)
    - WEST:  0x8 (1000)

    Used with bitwise operations to manage walls in maze cells.
    """

    NORTH = 0x1
    EAST = 0x2
    SOUTH = 0x4
    WEST = 0x8


class Direction(Enum):
    """Enumeration of the four cardinal directions.

    Each direction maps to its corresponding Wall value and provides
    a property to get the opposite direction.

    Attributes:
        NORTH: Direction pointing up
        EAST: Direction pointing right
        SOUTH: Direction pointing down
        WEST: Direction pointing left
    """

    NORTH = Wall.NORTH
    EAST = Wall.EAST
    SOUTH = Wall.SOUTH
    WEST = Wall.WEST

    @property
    def wall(self) -> Wall:
        """Get the Wall value corresponding to this direction.

        Returns:
            Wall: The wall enum value for this direction
        """
        return self.value

    @property
    def opposite(self) -> "Direction":
        """Get the opposite direction.

        Returns:
            Direction: The opposite direction (e.g., SOUTH for NORTH)
        """
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST:  Direction.WEST,
            Direction.WEST:  Direction.EAST,
        }[self]
