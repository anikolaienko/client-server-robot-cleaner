from robot.models.types import LevelType, LevelUpdateFunc, Direction, Position
from robot.algos.directions import NORTH, LEFT_TURN, RIGHT_TURN, OPPOSITE
from robot.algos.robot_cleaner import RobotCleaner
from robot.algos.level_utils import is_fully_cleaned


async def _turn_robot(robot: RobotCleaner, curr_direction: Direction, new_direction: Direction):
    if curr_direction == new_direction:
        return new_direction
    
    if LEFT_TURN[curr_direction] == new_direction:
        await robot.turnLeft()
    elif RIGHT_TURN[curr_direction] == new_direction:
        await robot.turnRight()
    else:
        await robot.turnLeft()
        await robot.turnLeft()
    return new_direction


async def _clean_level(robot: RobotCleaner, _direction: Direction) -> None:
    # TODO: think of a patterns: follow the wall, spiral outwards, spiral inwards
    # -1 - blocked
    #  0 - visited
    #  1 - to_visit
    curr_pos, curr_dir = (0, 0), _direction
    north_west, north_east, south_west, south_east = [], [], [[]], [[0]]
    sign_to_arr = {
        (True, True): (south_east, lambda row, col: (row, col)),
        (True, False): (south_west, lambda row, col: (row, col)),
        (False, True): (north_east, lambda row, col: (row, col)),
        (False, False): (north_west, lambda row, col: (row, col))
    }

    def is_visited(row: int, col: int) -> bool:
        arr, transform = sign_to_arr[(row >= 0, col >= 0)]
        row, col = transform(row, col)
        return row < len(arr) and col < len(arr[0]) and arr[row][col]
    
    def mark_visited(row: int, col: int) -> None:
        arr, transform = sign_to_arr[(row >= 0, col >= 0)]
        row, col = transform(row, col)
        arr[row][col] = 1
    
    def build_route(curr_pos, new_pos) -> list[Position]:
        ...

    def get_directions(curr_pos, curr_dir, new_pos) -> list[Direction]:
        route = build_route(curr_pos, new_pos)
        
    
    def move(new_pos) -> Position:
        ...

    to_visit = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # coordinates, not directions
    
    while to_visit:
        visit_pos = to_visit.pop()

        if is_visited(*visit_pos):
            # no need to go there, cause already visited
            continue

        directions = get_directions(curr_pos, curr_dir, visit_pos)
        while directions:
            next_direction = directions.pop()
            if next_direction == curr_dir:
                if await robot.move():
                    curr_pos = (curr_pos[0] + curr_dir[0], curr_pos[1] + curr_dir[1])
                else:
                    # TODO: what to do here?
                    ...
            else:
                curr_dir = await _turn_robot(robot, curr_dir, next_direction)

        await robot.clean()

        to_visit.extend([
            (curr_pos, LEFT_TURN[curr_dir]),
            (curr_pos, RIGHT_TURN[curr_dir]),
            (curr_pos, curr_dir)
        ])
        mark_visited(*curr_pos)


async def clean_level(name: str, level: LevelType, update_level: LevelUpdateFunc) -> bool:
    init_direction = NORTH
    robot = RobotCleaner(level, update_level, init_direction)
    await robot.clean()

    await _clean_level(robot, init_direction)

    return is_fully_cleaned(level)
