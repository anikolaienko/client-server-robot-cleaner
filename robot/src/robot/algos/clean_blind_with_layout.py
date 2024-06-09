from robot.types import LevelType, LevelUpdateFunc
from robot.models import Direction, Position
from robot.models.directions import NORTH
from robot.algos.robot_cleaner import RobotCleaner
from robot.algos.level_utils import is_fully_cleaned
from robot.algos.layout_builder import LayoutBuilder


async def _clean_level(robot: RobotCleaner, _direction: Direction) -> None:
    # TODO: think of a patterns: follow the wall, spiral outwards, spiral inwards
    curr_pos, curr_dir = Position(0, 0), _direction
    to_visit = [Position(0, -1), Position(1, 0), Position(0, 1), Position(-1, 0)]  # initial visit coordinates
    layout = LayoutBuilder()
    
    while to_visit:
        visit_pos = to_visit.pop()

        if layout.is_visited(visit_pos) or layout.is_blocked(visit_pos):
            # no need to go there, cause already visited
            continue

        directions = layout.get_directions(curr_pos, curr_dir, visit_pos)
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
                    layout.mark_visited(curr_pos)
                    await robot.clean()
                else:
                    layout.mark_blocked(new_pos)
        
        if curr_pos == visit_pos: # is successfully moved to destination
            to_visit.extend([
                curr_pos + curr_dir.turn_left(),
                curr_pos + curr_dir.turn_right(),
                curr_pos + curr_dir
            ])


async def clean_level(name: str, level: LevelType, update_level: LevelUpdateFunc) -> bool:
    init_direction = NORTH
    robot = RobotCleaner(level, update_level, init_direction)
    await robot.clean()

    await _clean_level(robot, init_direction)

    return is_fully_cleaned(level)
