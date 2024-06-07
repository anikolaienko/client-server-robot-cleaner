from robot.models.types import LevelType, LevelUpdateFunc, Direction
from robot.models.stats import Stats
from robot.algos.directions import LEFT_TURN, RIGHT_TURN
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
        row, col = (self._position[0] + self._direction[0], self._position[1] + self._direction[1])
        if not is_within_level(self._level, row, col) or self._level[row][col] == "x":
            self._stats.failed_moves += 1
            await self._update_level(self._level, self._stats, self._direction)
            return False
        
        self._level[self._position[0]][self._position[1]] = " "
        self._level[row][col] = "R"

        self._position = (row, col)
        self._stats.moves += 1
        await self._update_level(self._level, self._stats, self._direction)
        return True

    async def turnLeft(self) -> None:
        """
        Robot will stay on the same cell after calling turnLeft.
        Each turn will be 90 degrees.
        """
        self._direction = LEFT_TURN[self._direction]
        self._stats.turns += 1
        await self._update_level(self._level, self._stats, self._direction)
    
    async def turnRight(self) -> None:
        """
        Robot will stay on the same cell after calling turnRight.
        Each turn will be 90 degrees.
        """
        self._direction = RIGHT_TURN[self._direction]
        self._stats.turns += 1
        await self._update_level(self._level, self._stats, self._direction)

    async def clean(self) -> None:
        """Clean the current cell."""
        # nothing is really required to do here
        pass
