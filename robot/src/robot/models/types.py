from typing import Callable, Awaitable, Optional

from robot.models.stats import Stats


LevelType = list[list[str]]
Position = tuple[int, int]
Direction = tuple[int, int]
LevelUpdateFunc = Callable[[list[list[str]], Stats, Optional[Direction]], Awaitable[bool]]
