from robot.models.types import LevelType, Position


def find_start(level: LevelType) -> Position:
    for row_idx in range(len(level)):
        row = level[row_idx]
        for col_idx in range(len(row)):
            if row[col_idx] == "R":
                return row_idx, col_idx
    
    raise ValueError(f"No starting position found on level.")


def is_within_level(level: LevelType, row: int, col: int):
    rows, cols = len(level), len(level[0])

    return row >= 0 and row < rows and col >= 0 and col < cols


def is_fully_cleaned(level: LevelType) -> bool:
    rows = len(level)
    cols = len(level[0])

    return all(level[row][col] != "-" for row in range(rows) for col in range(cols))
