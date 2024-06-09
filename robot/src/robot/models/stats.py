class Stats:
    __slots__ = ["_moves", "_failed_moves", "_turns"]

    def __init__(self):
        self._moves = 0
        self._failed_moves = 0
        self._turns = 0

    def inc_moves(self):
        self._moves += 1

    def inc_turns(self):
        self._turns += 1
    
    def inc_failed_moves(self):
        self._failed_moves += 1

    def __str__(self) -> str:
        return f"Moves (attempted): {self._moves} ({self._moves + self._failed_moves}), Turns: {self._turns}"