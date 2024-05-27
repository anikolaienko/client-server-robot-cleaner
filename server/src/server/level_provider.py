from typing import Optional
from pathlib import Path

LEVELS_DIR = Path(__file__).parents[1] / "data" / "levels"


def _get_level_filepath(level_name: str) -> Path:
    return LEVELS_DIR / f"{level_name}.txt"


def get_level(level_name: str) -> Optional[str]:
    filepath = _get_level_filepath(level_name)
    if not filepath.exists():
        return None
    
    with open(filepath, "r") as file:
        return file.read()
