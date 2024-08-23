from dataclasses import dataclass
from typing import List
from copy import deepcopy


@dataclass
class Coord:
    row: int
    col: int

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(self.row) ^ hash(self.col)


@dataclass
class Image:
    rows: int
    cols: int
    galaxies: List[Coord]


def expand_empty_space(image: Image, addition: int) -> Image:
    """Duplicate empty rows and columns."""
    image = deepcopy(image)

    # Duplicate empty rows:
    row = 0
    while row < image.rows:
        empty = True
        for galaxy in image.galaxies:
            if galaxy.row == row:
                empty = False
                break

        if empty:
            # Move all galaxies below down by 'n' rows:
            for galaxy in image.galaxies:
                if galaxy.row > row:
                    galaxy.row = galaxy.row + addition
            row += addition
            image.rows += addition  # Increase total row count
        row += 1

    # Duplicate empty columns:
    col = 0
    while col < image.cols:
        empty = True
        for galaxy in image.galaxies:
            if galaxy.col == col:
                empty = False
                break

        if empty:
            # Move all galaxies to the right by 'n' columns:
            for galaxy in image.galaxies:
                if galaxy.col > col:
                    galaxy.col += addition

            col += addition
            image.cols += addition  # Also advice the row iterator doubly
        col += 1

    return image


def sum_closest_distance(image: Image) -> int:
    """Get sum of distances between all galaxy pairs."""
    dist_sum = 0

    # Find sum of shortest distance:
    for idx_1, galaxy_1 in enumerate(image.galaxies[:-1]):
        for idx_2, galaxy_2 in enumerate(image.galaxies[idx_1 + 1 :]):
            dist = abs(galaxy_2.row - galaxy_1.row) + abs(galaxy_2.col - galaxy_1.col)
            dist_sum += dist

    return dist_sum


def main():

    with open("input.txt", "r") as fh:

        image = Image(rows=0, cols=0, galaxies=[])

        # Load all data:
        while line := fh.readline():
            for col, char in enumerate(line):
                if char == "#":
                    coord = Coord(row=image.rows, col=col)
                    image.galaxies.append(coord)

            image.rows += 1
    image.cols = col + 1

    image_one = expand_empty_space(image, addition=1)
    dist_sum_one = sum_closest_distance(image_one)
    print(f"Sum of shortest distances is: {dist_sum_one}")

    # Now again after ultra-expand:

    image_million = expand_empty_space(image, addition=1_000_000 - 1)
    dist_sum_million = sum_closest_distance(image_million)
    print(f"Sum of shortest distances is: {dist_sum_million}")


if __name__ == "__main__":
    main()
