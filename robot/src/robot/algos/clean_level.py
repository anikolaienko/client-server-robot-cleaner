from typing import Tuple, Callable, Awaitable
from heapq import heappush, heappop

from robot.models.types import LevelType
from robot.algos.clean_level_configs import get_directions

LevelPositionType = Tuple[int, int]
LevelUpdateFunc = Callable[[list[list[str]]], Awaitable[bool]]


def _find_start(level: LevelType) -> LevelPositionType:
    for row_idx in range(len(level)):
        row = level[row_idx]
        for col_idx in range(len(row)):
            if row[col_idx] == "R":
                return row_idx, col_idx
    
    raise ValueError(f"No starting position found on level.")

def _within_level(level: LevelType, row: int, col: int):
    rows = len(level)
    cols = len(level[0])

    return row >= 0 and row < rows and col >= 0 and col < cols


def _find_next_near_position(
        level: LevelType,
        curr_pos: LevelPositionType,
        directions: list[tuple[int, int]]
    ) -> LevelPositionType:
    row, col = curr_pos

    for row_delta, col_delta in directions:
        row1, col1 = row + row_delta, col + col_delta
        
        if _within_level(level, row1, col1) and level[row1][col1] == "-":
            return row1, col1
    
    return None

def _find_route_to_not_visited_position(
        level: LevelType,
        curr_pos: LevelPositionType,
        directions: list[tuple[int, int]]
    ) -> list[LevelPositionType]:
    visited = set()
    parent = dict()
    queue = [(0, curr_pos)]

    while queue:
        score, pos = heappop(queue)
        if pos in visited:
            continue
        
        row, col = pos
        for row_delta, col_delta in directions:
            row1, col1 = row + row_delta, col + col_delta
            new_pos = (row1, col1)

            if _within_level(level, row1, col1) and new_pos not in visited:
                if level[row1][col1] == "-":
                    # build route and return
                    route = [new_pos]
                    while pos in parent:
                        route.append(pos)
                        pos = parent[pos]

                    return reversed(route)
                
                if level[row1][col1] == " ":
                    parent[new_pos] = pos
                    heappush(queue, (score + 1, new_pos))

        visited.add(pos)

    return []


async def clean_level(name: str, level: LevelType, update_level: LevelUpdateFunc) -> None:
    curr_pos = _find_start(level)
    directions = get_directions(name)

    while True:
        next_pos = _find_next_near_position(level, curr_pos, directions)

        if next_pos is not None:
            level[curr_pos[0]][curr_pos[1]] = " "
            level[next_pos[0]][next_pos[1]] = "R"
            curr_pos = next_pos

            if not await update_level(level):
                return
        else:
            route = _find_route_to_not_visited_position(level, curr_pos, directions)
            if not route:
                return

            for next_pos in route:
                level[curr_pos[0]][curr_pos[1]] = " "
                level[next_pos[0]][next_pos[1]] = "R"
                curr_pos = next_pos

                if not await update_level(level):
                    return
