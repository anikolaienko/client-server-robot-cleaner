from robot.robot_configs.config_provider import get_algo_configs
from robot.logger import log_success, log_error
from robot.algos.directions import NORTH, SOUTH, EAST, WEST

ALGO_NAME = "clean"
STR_TO_DIRECTION = {
    "NORTH": NORTH,
    "SOUTH": SOUTH,
    "EAST": EAST,
    "WEST": WEST,
}
DEFAULT_DIRECTIONS = [NORTH, WEST, SOUTH, EAST]


def get_directions(robot_name: str) -> list[tuple[int, int]]:
    configs = get_algo_configs(robot_name, ALGO_NAME)
    if not configs:
        return DEFAULT_DIRECTIONS
    
    try:
        directions = [
            STR_TO_DIRECTION[str(direction).upper()]
            for direction in configs["directions"]
        ]
        log_success(f"Loaded config for algo `{ALGO_NAME}`")
        return directions
    except Exception as ex:
        log_error(f"Failed load algo configs for {ALGO_NAME} algo. Error: {ex}. Using default.")
        return DEFAULT_DIRECTIONS
