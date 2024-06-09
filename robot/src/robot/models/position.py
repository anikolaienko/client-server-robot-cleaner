from dataclasses import dataclass, field

from .direction import Direction


@dataclass(frozen=True, slots=True)
class Position:
    """Robot position (row, col) in level layout."""
    row: int
    col: int

    def __add__(self, direction: "Direction") -> "Position":
        return Position(self.row + direction.row_delta, self.col + direction.col_delta)

    def __hash__(self) -> int:
        return hash((self.row, self.col))
    
    def __lt__(self, position: "Position") -> bool:
        return self.row < position.row or self.col < position.col
