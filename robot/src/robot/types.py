from typing import Callable, Awaitable

from robot.models import Stats, Direction


LevelType = list[list[str]]
LevelUpdateFunc = Callable[[list[list[str]], Stats, Direction], Awaitable[bool]]
