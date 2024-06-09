from heapq import heappush, heappop

from robot.types import LevelType, LevelUpdateFunc
from robot.models import Position, Direction
from robot.config.robot_config_provider import get_directions
from robot.algos.level_utils import is_within_level, is_fully_cleaned
from robot.algos.robot_cleaner import RobotCleaner


def _find_route_to_next_position(
        level: LevelType,
        curr_pos: Position,
        pref_directions: list[Direction]
    ) -> list[Position]:
    queue = [(0, curr_pos)]
    parents = {curr_pos: curr_pos}

    while queue:
        score, pos = heappop(queue)

        for direction in pref_directions:
            new_pos = pos + direction

            if is_within_level(level, new_pos) and new_pos not in parents:
                if level[new_pos.row][new_pos.col] == "-":    # good position, build and return the route 
                    route = [new_pos]
                    while pos != parents[pos]:        # until position parent is position itself: start position
                        route.append(pos)
                        pos = parents[pos]

                    return route
                
                if level[new_pos.row][new_pos.col] == " ":    # already cleaned position, continue searching
                    parents[new_pos] = pos
                    heappush(queue, (score + 1, new_pos))

    return []


def _get_directions(
        level: LevelType,
        curr_pos: Position,
        curr_dir: Direction,
        pref_directions: list[Direction]
    ) -> list[tuple[str, Position, Direction]]:
    directions = []
    route = _find_route_to_next_position(level, curr_pos, pref_directions)

    while route:
        pos = route.pop()

        if pos != (curr_pos + curr_dir):
            # need to turn
            if pos == (curr_pos + curr_dir.turn_left()):
                curr_dir = curr_dir.turn_left()
                directions.append(("left", curr_pos, curr_dir))
            elif pos == (curr_pos + curr_dir.turn_right()):
                curr_dir = curr_dir.turn_right()
                directions.append(("right", curr_pos, curr_dir))
            else:
                curr_dir = curr_dir.turn_left()
                directions.append(("left", curr_pos, curr_dir))
                curr_dir = curr_dir.turn_left()
                directions.append(("left", curr_pos, curr_dir))

        curr_pos = curr_pos + curr_dir
        directions.append(("move", curr_pos, curr_dir))
    
    return list(reversed(directions))


async def _clean_level(robot: RobotCleaner, level: LevelType, pref_directions: list[Direction]) -> None:
    curr_pos, curr_dir = robot._position, robot._direction

    while True:
        directions = _get_directions(level, curr_pos, curr_dir, pref_directions)
        if not directions:
            return is_fully_cleaned(level)
        
        while directions:
            command, new_pos, new_dir = directions.pop()
            if command == "left":
                await robot.turnLeft()
                curr_dir = new_dir
            elif command == "right":
                await robot.turnRight()
                curr_dir = new_dir
            else:
                if await robot.move():
                    curr_pos = new_pos
                    await robot.clean()


async def clean_level(name: str, level: LevelType, update_level: LevelUpdateFunc) -> bool:
    directions = get_directions(name)
    robot = RobotCleaner(level, update_level, directions[0])
    await robot.clean()

    await _clean_level(robot, level, directions)

    return is_fully_cleaned(level)
