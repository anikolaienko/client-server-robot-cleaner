from pathlib import Path
from typing import Any

from yaml import safe_load

from robot.logger import log_warning, log_success, log_error
from robot.models import Direction
from robot.models.directions import NORTH, SOUTH, EAST, WEST

ALGO_NAME = "clean"
DEFAULT_DIRECTIONS = [NORTH, WEST, SOUTH, EAST]
CONFIGS_DATA_DIR = Path(__file__).parents[2] / "data" / "robot_configs"


def get_algo_configs(robot_name: str, algo: str) -> dict[str, Any]:
    filepath = CONFIGS_DATA_DIR / f"{robot_name.capitalize()}.yml"

    if not filepath.exists():
        log_warning(f"Robot `{robot_name}` does not have any configs for algo `{algo}`. Using default configs.")
        return {}

    with open(filepath, "r") as f:
        configs = safe_load(f)
        if "algos" not in configs or algo not in configs["algos"]:
            log_warning(
                f"Robot `{robot_name}` does not have configs specifically for algo `{algo}`. Using default configs."
            )
            return {}
    
    return configs["algos"][algo]


def get_directions(robot_name: str) -> list[Direction]:
    configs = get_algo_configs(robot_name, ALGO_NAME)
    if not configs:
        return DEFAULT_DIRECTIONS
    
    try:
        directions = [
            Direction.parse(str(direction))
            for direction in configs["directions"]
        ]
        log_success(f"Loaded config for algo `{ALGO_NAME}`")
        return directions
    except Exception as ex:
        log_error(f"Failed load algo configs for {ALGO_NAME} algo. Error: {ex}. Using default.")
        return DEFAULT_DIRECTIONS
