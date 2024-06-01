from typing import Callable, Awaitable

LevelType = list[list[str]]
Position = tuple[int, int]
Direction = tuple[int, int]
LevelUpdateFunc = Callable[[list[list[str]]], Awaitable[bool]]
