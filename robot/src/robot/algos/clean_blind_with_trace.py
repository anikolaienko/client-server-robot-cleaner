from robot.types import LevelType, LevelUpdateFunc
from robot.models import Position, Direction
from robot.models.directions import NORTH
from robot.algos.robot_cleaner import RobotCleaner
from robot.algos.level_utils import is_fully_cleaned


async def _turn_robot(robot: RobotCleaner, curr_direction: Direction, new_direction: Direction):
    if curr_direction == new_direction:
        return new_direction
    
    if curr_direction.turn_left() == new_direction:
        await robot.turnLeft()
    elif curr_direction.turn_right() == new_direction:
        await robot.turnRight()
    else:
        await robot.turnLeft()
        await robot.turnLeft()
    return new_direction


async def _clean_level(robot: RobotCleaner, _direction: Direction) -> None:
    # TODO: think of a patterns: follow the wall, spiral outwards, spiral inwards
    curr_pos, curr_dir = Position(0, 0), _direction
    visited = set([curr_pos])
    trace = []
    
    to_visit = [
        (curr_pos, dir)
        for dir in (curr_dir.opposite(), curr_dir.turn_left(), curr_dir.turn_right(), curr_dir)
    ]
    
    while to_visit:
        visit_pos, visit_dir = to_visit.pop()

        new_pos = visit_pos + visit_dir
        if new_pos in visited:
            # no need to go there, cause already visited
            continue

        # lets move back until we are at the correct position
        while curr_pos != visit_pos:
            trace_direction = trace.pop()
            curr_dir = await _turn_robot(robot, curr_dir, trace_direction)
            await robot.move()
            curr_pos = curr_pos + curr_dir

        curr_dir = await _turn_robot(robot, curr_dir, visit_dir)

        if await robot.move():
            curr_pos = new_pos
            trace.append(curr_dir.opposite())
            to_visit.extend([
                (new_pos, curr_dir.turn_left()),
                (new_pos, curr_dir.turn_right()),
                (new_pos, curr_dir)
            ])
            await robot.clean()

        visited.add(new_pos)
        

async def clean_level(name: str, level: LevelType, update_level: LevelUpdateFunc) -> bool:
    init_direction = NORTH
    robot = RobotCleaner(level, update_level, init_direction)
    await robot.clean()

    await _clean_level(robot, init_direction)

    return is_fully_cleaned(level)
