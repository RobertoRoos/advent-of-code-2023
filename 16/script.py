import math
from dataclasses import dataclass
from typing import List, Tuple, Set
from enum import Enum


class Direction(Enum):
    """Direction traveling light."""

    UP = 1
    DOWN = -1
    RIGHT = 2
    LEFT = -2

    def __abs__(self):
        return Direction(abs(self.value))


@dataclass
class Tile:
    """Single tile content.

    Track if light is passing through horizontally and/or vertically.
    """

    char: str
    lit: Set[Direction]


class Contraption:
    """Instance of a mirrors board."""

    def __init__(self):
        # Board contents:
        self.tiles: List[List[Tile]] = []
        self.rows = 0
        self.cols = 0
        # ^ index as [row][col]

    def add_row(self, txt: str):
        new_row = [Tile(char=char, lit=set()) for col, char in enumerate(txt.strip())]
        self.cols = len(new_row)
        self.tiles.append(new_row)
        self.rows += 1

    def propagate_light(self, row: int, col: int, direction: Direction):
        """Recursively propagate a beam of light, modified the board in-place.

        The method starts by moving the beam.
        """
        while True:
            row, col = self.move(row, col, direction)
            if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                return  # Light hit the edge, discard
            tile = self.tiles[row][col]
            if direction in tile.lit:
                return  # Already travelled here this way
            tile.lit.add(direction)

            # Split horizontal or vertical:
            if tile.char == "-" and abs(direction) == Direction.UP:
                self.propagate_light(row, col, Direction.LEFT)
                self.propagate_light(row, col, Direction.RIGHT)
                return
            if tile.char == "|" and abs(direction) == Direction.RIGHT:
                self.propagate_light(row, col, Direction.UP)
                self.propagate_light(row, col, Direction.DOWN)
                return

            # Continue
            direction = self.mirror(direction, tile.char)

    @staticmethod
    def move(row: int, col: int, direction: Direction) -> Tuple[int, int]:
        if direction == Direction.UP:
            row -= 1
        elif direction == Direction.RIGHT:
            col += 1
        elif direction == Direction.DOWN:
            row += 1
        else:
            col -= 1
        return row, col

    @staticmethod
    def mirror(direction: Direction, char: str) -> Direction:
        if char != "\\" and char != "/":
            return direction

        new_abs_val = 2 if abs(direction.value) == 1 else 1
        new_val = math.copysign(new_abs_val, direction.value)
        if char == "\\":
            new_val *= -1

        return Direction(new_val)

    def print_lit(self):
        for row in self.tiles:
            for tile in row:
                char = "#" if tile.lit else "."
                print(char, end="")
            print()
        print()


def main():

    # Complete board:
    contraption = Contraption()

    with open("input.txt", "r") as fh:
        while line := fh.readline():
            contraption.add_row(line)

    contraption.propagate_light(0, -1, Direction.RIGHT)

    contraption.print_lit()

    value = len([tile for row in contraption.tiles for tile in row if tile.lit])

    print("Number:", value)


if __name__ == "__main__":
    main()
