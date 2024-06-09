from robot.types import LevelType
from robot.models import Position


def find_start(level: LevelType) -> Position:
    try:
        return next(
            Position(r, c)
            for r in range(len(level)) for c in range(len(level[r]))
            if level[r][c] == "R"
        )
    except StopIteration:
        raise ValueError(f"No starting position 'R' found on the level.")


def is_within_level(level: LevelType, pos: Position):
    return pos.row >= 0 and pos.row < len(level) and pos.col >= 0 and pos.col < len(level[0])


def is_fully_cleaned(level: LevelType) -> bool:
    return all(cell != "-" for row in level for cell in row)
