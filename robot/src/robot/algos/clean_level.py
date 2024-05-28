from typing import Callable, Awaitable
from heapq import heappush, heappop

from robot.models.types import LevelType
from robot.algos.clean_level_configs import get_directions

Position = tuple[int, int]
LevelUpdateFunc = Callable[[list[list[str]]], Awaitable[bool]]


def _find_start(level: LevelType) -> Position:
    for row_idx in range(len(level)):
        row = level[row_idx]
        for col_idx in range(len(row)):
            if row[col_idx] == "R":
                return row_idx, col_idx
    
    raise ValueError(f"No starting position found on level.")


def _all_clean(level: LevelType) -> bool:
    rows = len(level)
    cols = len(level[0])

    return all(level[row][col] != "-" for row in range(rows) for col in range(cols))


def _within_level(level: LevelType, row: int, col: int):
    rows = len(level)
    cols = len(level[0])

    return row >= 0 and row < rows and col >= 0 and col < cols


def _find_route_to_next_position(
        level: LevelType,
        curr_pos: Position,
        directions: list[tuple[int, int]],
    ) -> list[Position]:
    parents = {curr_pos: curr_pos}
    queue = [(0, curr_pos)]

    while queue:
        score, pos = heappop(queue)

        row, col = pos
        for row_delta, col_delta in directions:
            new_row, new_col = row + row_delta, col + col_delta
            new_pos = (new_row, new_col)

            if _within_level(level, new_row, new_col) and new_pos not in parents:
                if level[new_row][new_col] == "-":    # good position, build and return the route 
                    route = [new_pos]
                    while pos != parents[pos]:        # until position parent is position itself: start position
                        route.append(pos)
                        pos = parents[pos]

                    return reversed(route)
                
                if level[new_row][new_col] == " ":    # already cleaned position, continue searching
                    parents[new_pos] = pos
                    heappush(queue, (score + 1, new_pos))

    return []


async def clean_level(name: str, level: LevelType, update_level: LevelUpdateFunc) -> bool:
    curr_pos = _find_start(level)
    directions = get_directions(name)

    while True:
        route = _find_route_to_next_position(level, curr_pos, directions)
        if not route:
            return _all_clean(level)

        for next_pos in route:
            level[curr_pos[0]][curr_pos[1]] = " "
            level[next_pos[0]][next_pos[1]] = "R"
            curr_pos = next_pos

            if not await update_level(level):
                return False
