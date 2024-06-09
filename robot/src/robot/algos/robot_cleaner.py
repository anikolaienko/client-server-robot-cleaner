from robot.types import LevelType, LevelUpdateFunc
from robot.models import Direction
from robot.models.stats import Stats
from robot.algos.level_utils import find_start, is_within_level


class RobotCleaner:
    def __init__(self, level: LevelType, update_level: LevelUpdateFunc, direction: Direction):
        self._level = level
        self._update_level = update_level
        self._position = find_start(level)
        self._direction = direction
        self._stats = Stats()

    async def move(self) -> bool:
        """
        Returns true if next cell is open and robot moves into the cell.
        Returns false if next cell is obstacle and robot stays on the current cell.
        """
        new_pos = self._position + self._direction
        if not is_within_level(self._level, new_pos) or self._level[new_pos.row][new_pos.col] == "x":
            self._stats.inc_failed_moves()
            await self._update_level(self._level, self._stats, self._direction)
            return False
        
        self._level[self._position.row][self._position.col] = " "
        self._level[new_pos.row][new_pos.col] = "R"

        self._position = new_pos
        self._stats.inc_moves()
        await self._update_level(self._level, self._stats, self._direction)
        return True

    async def turnLeft(self) -> None:
        """
        Robot will stay on the same cell after calling turnLeft.
        Each turn will be 90 degrees.
        """
        self._direction = self._direction.turn_left()
        self._stats.inc_turns()
        await self._update_level(self._level, self._stats, self._direction)
    
    async def turnRight(self) -> None:
        """
        Robot will stay on the same cell after calling turnRight.
        Each turn will be 90 degrees.
        """
        self._direction = self._direction.turn_right()
        self._stats.inc_turns()
        await self._update_level(self._level, self._stats, self._direction)

    async def clean(self) -> None:
        """Clean the current cell."""
        # nothing is really required to do here
        pass
