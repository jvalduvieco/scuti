from dataclasses import dataclass, field, replace
from typing import Dict, Tuple, List

from domain.games.types import PlayerId
from infrastructure.tools.list import all_equal_and_not_none


@dataclass(frozen=True)
class TicTacToeBoard:
    cells: Dict[Tuple[int, int], PlayerId] = field(default_factory=dict)

    def place(self, x: int, y: int, player_id: PlayerId):
        self.__assert_valid_position(x, y)
        if not self.is_cell_free(x, y):
            raise ValueError(f"Cell {x},{y} already used")

        return replace(self, cells={**self.cells, (x, y): player_id})

    def is_cell_free(self, x: int, y: int) -> bool:
        return self.cells.get((x, y), None) is None

    def is_full(self) -> bool:
        return len(self.cells.items()) == 9

    def is_off_limits(self, x: int, y: int) -> bool:
        return x > 2 or y > 2

    def to_list(self) -> List[List[PlayerId | None]]:
        result = []
        for y in range(3):
            row = []
            for x in range(3):
                row += [self[x, y]]
            result.append(row)
        return result

    def any_player_has_three_in_a_row(self) -> PlayerId | None:
        if all_equal_and_not_none([self.cells.get(position, None) for position in [(0, 0), (1, 0), (2, 0)]]):
            return self.cells[0, 0]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(0, 1), (1, 1), (2, 1)]]):
            return self.cells[0, 1]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(0, 2), (1, 2), (2, 2)]]):
            return self.cells[0, 2]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(0, 0), (0, 1), (0, 2)]]):
            return self.cells[0, 0]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(1, 0), (1, 1), (1, 2)]]):
            return self.cells[1, 0]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(2, 0), (2, 1), (2, 2)]]):
            return self.cells[2, 0]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(0, 0), (1, 1), (2, 2)]]):
            return self.cells[0, 0]
        elif all_equal_and_not_none([self.cells.get(position, None) for position in [(2, 0), (1, 1), (0, 2)]]):
            return self.cells[2, 0]
        return None

    def __getitem__(self, item) -> PlayerId | None:
        return self.cells.get(item, None)

    def __assert_valid_position(self, x, y):
        if x > 2:
            raise ValueError(f"Invalid value {x} for x")
        if y > 2:
            raise ValueError(f"Invalid value {y} for y")
