from enum import IntEnum, Enum


class Wall(IntEnum):
    NORTH = 0x1
    EAST = 0x2
    SOUTH = 0x4
    WEST = 0x8


class Direction(Enum):
    NORTH = Wall.NORTH
    EAST = Wall.EAST
    SOUTH = Wall.SOUTH
    WEST = Wall.WEST

    @property
    def wall(self):
        return self.value

    @property
    def opposite(self):
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST:  Direction.WEST,
            Direction.WEST:  Direction.EAST,
        }[self]
