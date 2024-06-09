from heapq import heappush, heappop

from robot.models import Position, Direction
from robot.models.directions import NORTH, SOUTH, EAST, WEST

_BLOCKED = -1
_VACANT = 0
_VISITED = 1


class LayoutBuilder:
    def __init__(self):
        north_west, north_east, south_west, south_east = [], [], [[]], [[_VISITED]]
        self._sign_to_arr = {
            (True, True): (south_east, lambda pos: Position(pos.row, pos.col)),
            (True, False): (south_west, lambda pos: Position(pos.row, -pos.col - 1)),
            (False, True): (north_east, lambda pos: Position(-pos.row - 1, pos.col)),
            (False, False): (north_west, lambda pos: Position(-pos.row - 1, -pos.col - 1))
        }

    def _get_arr_with_position(self, pos: Position) -> tuple[list[list[int]], Position]:
        arr, transform = self._sign_to_arr[(pos.row >= 0, pos.col >= 0)]
        return arr, transform(pos)

    def is_within_arr(self, arr: list[list[int]], pos: Position) -> bool:
        return len(arr) > 0 and pos.row < len(arr) and pos.col < len(arr[0])

    def is_visited(self, pos: Position) -> bool:
        arr, pos = self._get_arr_with_position(pos)
        return self.is_within_arr(arr, pos) and arr[pos.row][pos.col] == _VISITED
    
    def is_blocked(self, pos: Position) -> bool:
        arr, pos = self._get_arr_with_position(pos)
        return self.is_within_arr(arr, pos) and arr[pos.row][pos.col] == _BLOCKED
    
    def expand(self, arr: list[list[int]], pos: Position) -> None:
        while pos.row >= len(arr):
            cols_delta = len(arr[0]) if len(arr) > 0 else 1
            arr.append([_VACANT] * cols_delta)
        
        if pos.col >= len(arr[pos.row]):
            cols_delta = pos.col - len(arr[0]) + 1
            for arr_row in arr:
                arr_row.extend([_VACANT] * cols_delta)

    def mark_visited(self, pos: Position) -> None:
        arr, pos = self._get_arr_with_position(pos)
        self.expand(arr, pos)
        arr[pos.row][pos.col] = _VISITED

    def mark_blocked(self, pos: Position) -> None:
        arr, pos = self._get_arr_with_position(pos)
        self.expand(arr, pos)
        arr[pos.row][pos.col] = _BLOCKED

    def build_route(self, curr_pos: Position, searched_pos: Position) -> list[Position]:
        if curr_pos == searched_pos:
            return []
        
        queue = [(0, curr_pos)]
        parents = {curr_pos: curr_pos}

        while queue:
            score, pos = heappop(queue)

            for direction in [NORTH, WEST, SOUTH, EAST]:
                new_pos = pos + direction

                if new_pos == searched_pos:   # build and return the route
                    route = [new_pos]
                    while pos != parents[pos]:
                        route.append(pos)
                        pos = parents[pos]

                    return route
            
                if self.is_visited(new_pos) and new_pos not in parents:
                    parents[new_pos] = pos
                    heappush(queue, (score + 1, new_pos))
        
        return []

    def get_directions(
            self,
            curr_pos: Position,
            curr_dir: Direction,
            searched_pos: Position
        ) -> list[tuple[str, Position, Direction]]:
        directions = []
        route = self.build_route(curr_pos, searched_pos)

        while route:
            pos = route.pop()

            if pos != (curr_pos + curr_dir):
                # need to turn
                if pos == (curr_pos + curr_dir.turn_left()):
                    curr_dir = curr_dir.turn_left()
                    directions.append(("left", curr_pos, curr_dir))
                elif pos == (curr_pos + curr_dir.turn_right()):
                    curr_dir = curr_dir.turn_right()
                    directions.append(("right", curr_pos, curr_dir))
                else:
                    curr_dir = curr_dir.turn_left()
                    directions.append(("left", curr_pos, curr_dir))
                    curr_dir = curr_dir.turn_left()
                    directions.append(("left", curr_pos, curr_dir))

            curr_pos = curr_pos + curr_dir
            directions.append(("move", curr_pos, curr_dir))
        
        return list(reversed(directions))
