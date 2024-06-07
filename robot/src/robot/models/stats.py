from dataclasses import dataclass

@dataclass
class Stats:
    moves: int = 0
    turns: int = 0
    failed_moves: int = 0
