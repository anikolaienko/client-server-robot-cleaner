from robot.robot_configs.config_provider import get_algo_configs
from robot.logger import log_success, log_error

ALGO_NAME = "clean"
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STR_TO_DIRECTION = {
    "UP": UP,
    "DOWN": DOWN,
    "LEFT": LEFT,
    "RIGHT": RIGHT
}
DEFAULT_DIRECTIONS = [UP, LEFT, DOWN, RIGHT]


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
