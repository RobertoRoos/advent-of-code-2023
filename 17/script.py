from dataclasses import dataclass
from typing import List, Optional, NamedTuple, Dict, Tuple, DefaultDict
from collections import defaultdict
from enum import IntEnum
from queue import PriorityQueue
import math


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = -1
    WEST = -2


class Coord(NamedTuple):
    row: int
    col: int

    def __add__(self, other) -> "Coord":
        return Coord(self.row + other.row, self.col + other.col)

    def __sub__(self, other) -> "Coord":
        return Coord(self.row - other.row, self.col - other.col)


class CoordExtras(NamedTuple):
    straight_steps: int  # Numer of straight steps to get there
    direction: Optional[Direction]  # Entered here heading this direction


direction_steps: Dict[Direction, Coord] = {
    Direction.NORTH: Coord(-1, 0),
    Direction.EAST: Coord(0, 1),
    Direction.SOUTH: Coord(1, 0),
    Direction.WEST: Coord(0, -1),
}


@dataclass(order=True)
class State:
    """State of tile during path-finding.

    Instances are compared based on `cost` (actually fields in order).
    """

    cost: int  # Summed cost to get to this tile
    coord: Coord  # Coordinate of this state
    extras: CoordExtras  # Meta data


class Map:
    """Container for map of city blocks."""

    def __init__(self):
        self.blocks: Dict[Coord, int] = {}
        self.rows = 0
        self.cols = 0

    def add_row(self, line: str):
        if self.cols > 0:
            if len(line) != self.cols:
                raise ValueError(f"Invalid columns in {line}")
        else:
            self.cols = len(line)
        for i, c in enumerate(line):
            coord = Coord(self.rows, i)
            self.blocks[coord] = int(c)
        self.rows += 1

    def get_next_coords(self, tile: State) -> List[State]:
        """Return adjacent coordinates and tiles (that are valid)."""
        pass
        for next_dir in Direction:
            if (
                tile.extras.direction is not None
                and next_dir.value == -1 * tile.extras.direction.value
            ):
                continue  # Cannot flip direction

            next_straight_steps = 1  # Counting this current step
            if next_dir == tile.extras.direction:
                next_straight_steps = tile.extras.straight_steps + 1
                if next_straight_steps > 3:
                    continue  # This direction is not valid

            step = direction_steps[next_dir]
            next_coord = tile.coord + step
            if (
                next_coord.row < 0
                or next_coord.row >= self.rows
                or next_coord.col < 0
                or next_coord.col >= self.cols
            ):
                continue  # Hit the edge, skip

            next_extras = CoordExtras(
                straight_steps=next_straight_steps, direction=next_dir
            )

            next_tile = State(
                tile.cost + self.blocks[next_coord], next_coord, next_extras
            )

            yield next_tile

    def calculate_path(self) -> int:
        """Get the shortest path length."""
        start = Coord(0, 0)
        extras = CoordExtras(0, None)
        tiles: DefaultDict[Coord, Dict[CoordExtras, State]] = defaultdict(dict)
        tiles[start][extras] = State(0, start, extras)

        # All the tips we can possibly advance from:
        tips: PriorityQueue[State] = PriorityQueue()
        for s_list in tiles.values():
            for s in s_list.values():
                tips.put(s)

        while not tips.empty():

            tip: State = tips.get(timeout=False)

            for next_tile in self.get_next_coords(tip):
                existing_tile = tiles[next_tile.coord].get(next_tile.extras, None)

                if (
                    existing_tile is None or next_tile.cost < existing_tile.cost
                ):  # Found a better path:
                    tiles[next_tile.coord][next_tile.extras] = next_tile
                    tips.put(next_tile)

                    # self.print_tiles(tiles)
                    #
                    # print("Tips:")
                    # for tip in tips.queue:
                    #     print(tip)
                    # print()

        # Find fastest way out:
        final = Coord(self.rows - 1, self.cols - 1)
        options = tiles.get(final)
        return min(tile.cost for tile in options.values())

    def print_tiles(self, tiles):
        for row in range(self.rows):
            for col in range(self.cols):
                coord = Coord(row, col)
                weight = self.blocks[coord]
                print(weight, end="")
                count_str = f"({len(tiles[coord])})" if coord in tiles else "   "
                print(count_str, end="")
                print("\t", end="")
            print()
        print()


def main():

    my_map = Map()

    with open("input.txt", "r") as fh:
        while line := fh.readline():
            my_map.add_row(line.strip())

    value = my_map.calculate_path()

    print("Lowest cost:", value)


if __name__ == "__main__":
    main()
