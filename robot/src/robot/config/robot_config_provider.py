from pathlib import Path
from typing import Any

from yaml import safe_load

from robot.logger import log_warning

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
