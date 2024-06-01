from heapq import heappush, heappop

from robot.models.types import LevelType, Position, LevelUpdateFunc
from robot.algos.robot_config_provider import get_directions
from robot.algos.level_utils import find_start, is_within_level, is_fully_cleaned


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

            if is_within_level(level, new_row, new_col) and new_pos not in parents:
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
    curr_pos = find_start(level)
    directions = get_directions(name)

    while True:
        route = _find_route_to_next_position(level, curr_pos, directions)
        if not route:
            return is_fully_cleaned(level)

        for next_pos in route:
            level[curr_pos[0]][curr_pos[1]] = " "
            level[next_pos[0]][next_pos[1]] = "R"
            curr_pos = next_pos

            if not await update_level(level):
                return False
