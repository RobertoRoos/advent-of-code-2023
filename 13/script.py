from enum import Enum
from typing import List, Optional


class Tile(Enum):
    ROCK = "#"
    ASH = "."

    @staticmethod
    def get_list_from_text(txt: str) -> List["Tile"]:
        return [Tile(c) for c in txt]


Pattern = List[List[Tile]]


def find_horizontal_symmetry(pattern: Pattern) -> Optional[int]:
    """Returned index in the bottom row of the two."""
    for row_idx in range(1, len(pattern)):  # Try all mirror positions
        check_top_row_idx = row_idx - 1
        check_bottom_row_idx = row_idx
        symmetrical = True
        while check_top_row_idx >= 0 and check_bottom_row_idx < len(pattern):
            if pattern[check_bottom_row_idx] != pattern[check_top_row_idx]:
                symmetrical = False
                break
            check_top_row_idx -= 1
            check_bottom_row_idx += 1

        if symmetrical:
            return row_idx

    return None


def rotate_pattern(pattern: Pattern) -> Pattern:
    """Rotate the matrix 90 degrees.

    Such that the bottom left item becomes the top right."""
    new_pattern: Pattern = []

    # Indices for new pattern:
    for row_idx in range(len(pattern[0])):
        new_row = []
        for col_idx in range(len(pattern)):
            new_row.append(pattern[col_idx][row_idx])
        new_pattern.append(new_row)

    return new_pattern


def get_score(pattern: Pattern) -> int:
    """Get the magic score based on symmetry in the pattern."""
    score = find_horizontal_symmetry(pattern)
    if score is not None:
        return score * 100

    pattern = rotate_pattern(pattern)
    score = find_horizontal_symmetry(pattern)
    if score is not None:
        return score

    raise ValueError("Found no symmetry at all!")


def main():

    total_score = 0

    with open("input.txt", "r") as fh:

        pattern: Pattern = []  # List of rows

        done = False
        while not done:
            line = fh.readline()
            if not line:
                done = True
            line = line.strip()
            if not line and pattern and pattern[0]:
                score = get_score(pattern)
                total_score += score
                pattern = []
                continue

            pattern.append(Tile.get_list_from_text(line))

    print("Score:", total_score)


if __name__ == "__main__":
    main()
