from dataclasses import dataclass, field
from functools import cached_property

__NORTH = (-1, 0)
__SOUTH = (1, 0)
__EAST = (0, 1)
__WEST = (0, -1)

_VALID_DIRECTIONS = set([
    __NORTH, __SOUTH, __EAST, __WEST
])

_LEFT_TURN = {
    __NORTH: __WEST,
    __WEST: __SOUTH,
    __SOUTH: __EAST,
    __EAST: __NORTH
}

_RIGHT_TURN = {
    __NORTH: __EAST,
    __EAST: __SOUTH,
    __SOUTH: __WEST,
    __WEST: __NORTH
}

_OPPOSITE = {
    __NORTH: __SOUTH,
    __SOUTH: __NORTH,
    __WEST: __EAST,
    __EAST: __WEST
}

_STR_TO_DIRECTION = {
    "NORTH": __NORTH,
    "SOUTH": __SOUTH,
    "EAST": __EAST,
    "WEST": __WEST,
}

_DIRECTION_TO_CHAR = {
    __NORTH: ":up_arrow-emoji:",
    __SOUTH: ":down_arrow-emoji:",
    __EAST: ":right_arrow-emoji:",
    __WEST: ":left_arrow-emoji:"
}

# alternative
# DIRECTION_TO_CHAR = {
#     NORTH: ":arrow_up_small-emoji:",
#     SOUTH: ":arrow_down_small-emoji:",
#     EAST: ":arrow_forward-emoji:",
#     WEST: ":arrow_backward-emoji:"
# }


@dataclass(frozen=True)
class Direction:
    row_delta: int
    col_delta: int

    def __post_init__(self) -> None:
        if self._value not in _VALID_DIRECTIONS:
            raise ValueError(f"Direction ({self._value}) is invalid, should be one of: {_VALID_DIRECTIONS}")

    @cached_property
    def _value(self) -> tuple[int, int]:
        return (self.row_delta, self.col_delta)
    
    @classmethod
    def parse(cls, value: str) -> "Direction":
        return Direction(*_STR_TO_DIRECTION[value.upper()])

    def turn_left(self) -> "Direction":
        return Direction(*_LEFT_TURN[self._value])
    
    def turn_right(self) -> "Direction":
        return Direction(*_RIGHT_TURN[self._value])
    
    def opposite(self) -> "Direction":
        return Direction(*_OPPOSITE[self._value])
    
    def __str__(self) -> str:
        return _DIRECTION_TO_CHAR[self._value]
