from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Dict, Optional

from pkg_resources import get_supported_platform


class Tile(Enum):
    ROUND = "O"  # Not actually a normal zero
    CUBE = "#"
    EMPTY = "."


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

    shift_up(platform)

    platform.print()

    score = get_weight(platform)
    print("Score:", score)


if __name__ == "__main__":
    main()
