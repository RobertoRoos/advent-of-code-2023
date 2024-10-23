from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Dict, Optional, List


class Tile(Enum):
    ROUND = "O"  # Not actually a normal zero
    CUBE = "#"
    EMPTY = "."


class Direction(Enum):
    NORTH = "north"
    WEST = "west"
    SOUTH = "south"
    EAST = "east"


class Coord(NamedTuple):
    row: int  # Horizontal row, counting 0 from the top
    col: int  # Vertical column, counting 0 from the left


# Platform = Dict[Coord, Tile]


@dataclass
class Platform:
    """Container for tiles by their coordinates."""

    tiles: Optional[Dict[Coord, Tile]] = None
    cols: int = 0
    rows: int = 0

    def add_tile(self, row, col, tile: Tile):
        if self.tiles is None:
            self.tiles = {}

        self.tiles[Coord(row, col)] = tile
        self.rows = max(self.rows, row + 1)
        self.cols = max(self.cols, col + 1)

    def print(self):
        for row in range(self.rows):
            for col in range(self.cols):
                tile = self.tiles.get(Coord(row, col), Tile.EMPTY)
                print(tile.value, end="")
            print()
        print()


def rotate_platform(platform: Platform, direction: Direction) -> Platform:
    """Rotate a platform, assuming currently North is up.

    Afterward the new direction is facing up.
    """
    new_platform = Platform()
    rows_max = platform.rows - 1  # Highest indices
    cols_max = platform.cols - 1
    for coord, tile in platform.tiles.items():
        if direction == Direction.WEST:
            new_coord = Coord(row=coord.col, col=rows_max - coord.row)
        elif direction == Direction.SOUTH:
            new_coord = Coord(row=rows_max - coord.row, col=cols_max - coord.col)
        elif direction == Direction.EAST:
            new_coord = Coord(row=cols_max - coord.col, col=coord.row)
        else:
            new_coord = coord

        new_platform.add_tile(new_coord.row, new_coord.col, tile)

    return new_platform


def cycle(platform: Platform) -> Platform:
    """Perform a single cycle on a platform (four shifts)."""
    for _ in range(4):
        shift_up(platform)
        platform = rotate_platform(platform, Direction.WEST)
        # Actually we only need to rotate 90° CW each time

    return platform  # By ending with a rotoation we got the original orientation back


def shift_up(platform: Platform):
    """Shift all round boulders up as far as they'll go."""
    for col in range(platform.cols):
        first_row_empty = None  # Row index an item could move into
        for row in range(platform.rows):
            coord = Coord(row, col)
            tile = platform.tiles.get(coord, None)  # Tile under consideration
            if tile is None:
                if first_row_empty is None:
                    first_row_empty = row  # We found the next empty spot
            elif tile == Tile.CUBE:
                first_row_empty = None  # We can't move anything past here
            elif tile == Tile.ROUND:
                if first_row_empty is not None:
                    # Move tile into there:
                    platform.tiles.pop(coord)  # Remove
                    new_coord = Coord(first_row_empty, col)
                    platform.tiles[new_coord] = tile  # Place again
                    first_row_empty += 1  # One spot got filled up


def get_weight(platform: Platform) -> int:
    """Get weight of round objects."""
    score = 0
    for coord, tile in platform.tiles.items():
        if tile != Tile.ROUND:
            continue
        score += platform.rows - coord.row
    return score


def get_weight_after_many_cycles(platform: Platform, number: int) -> int:
    """Keep repeating cycles for a set of times or until nothing changes."""
    loop: List[Optional[int]] = [None]  # [ Index MOD loop size: Score }
    loop_size = 1
    repitions = 0  # Number of full loops passed
    score = 0
    for idx in range(number):
        platform = cycle(platform)
        score = get_weight(platform)

        loop_idx = idx % loop_size

        if idx > 20:
            if any(x is None for x in loop):
                loop[loop_idx] = score
            else:
                if loop[loop_idx] == score:
                    if loop_idx == loop_size - 1:
                        repitions += 1
                else:
                    loop_size += 1  # Make search bigger
                    loop = [None] * loop_size  # And start again
                    repitions = 0

            if repitions >= 5:
                return loop[number % loop_size - 1]

    return score


def main():
    platform = Platform()
    with open("input.txt", "r") as fh:
        row = 0
        while line := fh.readline():
            line = line.strip()
            for col, char in enumerate(line):
                tile = Tile(char)
                if tile == Tile.EMPTY:
                    continue

                platform.add_tile(row, col, tile)
            row += 1

    platform.print()

    # Part 1:
    # shift_up(platform)

    # Part 2:
    score = get_weight_after_many_cycles(platform, 1000000000)

    print("Score:", score)


if __name__ == "__main__":
    main()
