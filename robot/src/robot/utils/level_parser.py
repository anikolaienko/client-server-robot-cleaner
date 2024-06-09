from robot.types import LevelType


def parse_level(level: str) -> LevelType:
    return list(
        filter(
            lambda row: row,
            (row.split() for row in level.split("\n"))
        )
    )
