from dataclasses import dataclass
from typing import List, Dict, Set, NamedTuple


@dataclass
class Coord:
    row: int
    col: int

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(self.row) ^ hash(self.col)


def main():

    with open("input.txt", "r") as fh:

        # Load all data:
        galaxies: List[Coord] = []
        row = 0
        while line := fh.readline():
            for col, char in enumerate(line):
                if char == "#":
                    coord = Coord(row=row, col=col)
                    galaxies.append(coord)

            row += 1

    rows = row
    cols = col + 1

    # Duplicate empty rows:
    row = 0
    while row < rows:
        empty = True
        for col in range(cols):
            if Coord(row=row, col=col) in galaxies:
                empty = False
                break

        if empty:
            # Move all galaxies below down by one row:
            for galaxy in galaxies:
                if galaxy.row > row:
                    galaxy.row = galaxy.row + 1
            row += 1
            rows += 1  # Increase total row count
        row += 1

    # Duplicate empty columns:
    col = 0
    while col < cols:
        empty = True
        for row in range(rows):
            if Coord(row=row, col=col) in galaxies:
                empty = False
                break

        if empty:
            # Move all galaxies to the right by one column:
            for galaxy in galaxies:
                if galaxy.col > col:
                    galaxy.col += 1

            col += 1
            cols += 1  # Also advice the row iterator doubly
        col += 1

    dist_sum = 0

    # Find sum of shortest distance:
    for idx_1, galaxy_1 in enumerate(galaxies[:-1]):
        for idx_2, galaxy_2 in enumerate(galaxies[idx_1 + 1:]):
            dist = abs(galaxy_2.row - galaxy_1.row) + abs(galaxy_2.col - galaxy_1.col)
            dist_sum += dist

    print(f"Sum of shortest distances is: {dist_sum}")


if __name__ == "__main__":
    main()
