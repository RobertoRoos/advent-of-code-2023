from dataclasses import dataclass
from typing import List, Optional, NamedTuple, Dict, DefaultDict
from collections import defaultdict
from enum import IntEnum
from queue import PriorityQueue


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


class PathInfo(NamedTuple):
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
    info: PathInfo  # Meta data


class Map:
    """Container for map of city blocks."""

    STRAIGHT_MIN = 0
    STRAIGHT_MAX = 3

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
            if tile.info.direction is not None:
                if next_dir.value == -1 * tile.info.direction:
                    continue  # Cannot go backwards

                if next_dir == tile.info.direction:
                    next_straight_steps = tile.info.straight_steps + 1
                    if next_straight_steps > self.STRAIGHT_MAX:
                        continue  # Not valid, cannot keep going straight
                else:
                    next_straight_steps = 1  # Counting this current step
                    if tile.info.straight_steps < self.STRAIGHT_MIN:
                        continue  # Not valid, cannot steer yet
            else:
                next_straight_steps = 1  # Not counting the very first block!

            step = direction_steps[next_dir]
            next_coord = tile.coord + step
            if (
                next_coord.row < 0
                or next_coord.row >= self.rows
                or next_coord.col < 0
                or next_coord.col >= self.cols
            ):
                continue  # Hit the edge, skip

            next_extras = PathInfo(
                straight_steps=next_straight_steps, direction=next_dir
            )

            next_tile = State(
                tile.cost + self.blocks[next_coord], next_coord, next_extras
            )

            yield next_tile

    def calculate_path(self) -> int:
        """Get the shortest path length."""
        # Create a cache list for all computed path tiles
        # This could have been a list, but we key it by coordinates
        # and info instead, such that we can do fast lookup
        start = Coord(0, 0)
        info = PathInfo(1, None)
        tiles: DefaultDict[Coord, Dict[PathInfo, State]] = defaultdict(dict)
        tiles[start][info] = State(0, start, info)

        # All the tips we can possibly advance from:
        tips: PriorityQueue[State] = PriorityQueue()
        for s_list in tiles.values():
            for s in s_list.values():
                tips.put(s)

        # Fill up the entire map, i.e. until no more tips are left:
        while not tips.empty():

            tip: State = tips.get(timeout=False)

            for next_tile in self.get_next_coords(tip):
                existing_tile = tiles[next_tile.coord].get(next_tile.info, None)

                if (
                    existing_tile is None or next_tile.cost < existing_tile.cost
                ):  # Found a better path:
                    tiles[next_tile.coord][next_tile.info] = next_tile
                    tips.put(next_tile)

                    # self.print_tiles(tiles)
                    # self.print_tips(tips)

        # Now find the value of the shortest way out:
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

    @staticmethod
    def print_tips(tips):
        print("Tips:")
        for tip in tips.queue:
            print(tip)
        print()


def main():

    my_map = Map()

    with open("input.txt", "r") as fh:
        while line := fh.readline():
            my_map.add_row(line.strip())

    value = my_map.calculate_path()

    # Part one answer: 1008
    print("Lowest cost:", value)


if __name__ == "__main__":
    main()
