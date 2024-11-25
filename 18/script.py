from typing import NamedTuple, List, Tuple
from enum import Enum
import numpy as np


class Direction(Enum):
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"
    UP = "U"


direction_to_coord = {
    Direction.RIGHT: np.array([1, 0]),
    Direction.DOWN: np.array([0, -1]),
    Direction.LEFT: np.array([-1, 0]),
    Direction.UP: np.array([0, 1]),
}

ListCoords = List[np.array]


class DigPlan:
    """Map of the dig plan."""

    def __init__(self):
        # As [x, y]:
        self.vertices: ListCoords = []
        self.range_min = np.array([0, 0])  # x, y
        self.range_max = np.array([0, 0])  # x, y

    def add_instruction(self, line: str):
        """Add a dig step."""
        dir_str, count, _ = line.split(" ")
        direction = Direction(dir_str)
        step = direction_to_coord[direction]
        tip = self.vertices[-1].copy() if self.vertices else np.array([0, 0])
        # When tip is a new [0, 0] it's not added yet, the last will also be [0, 0]
        tip += step * int(count)
        self.vertices.append(tip)
        for i in (0, 1):
            self.range_min[i] = np.min(np.array([self.range_min[i], tip[i]]))
            self.range_max[i] = np.max(np.array([self.range_max[i], tip[i]]))

    @property
    def border(self) -> ListCoords:
        for i, vertex in enumerate(self.vertices):
            next_vertex = self.vertices[(i + 1) % len(self.vertices)]
            diff = next_vertex - vertex
            count = int(np.linalg.norm(diff))
            step = diff / count
            for j in range(count):
                coord = vertex + j * step
                yield np.rint(coord).astype(np.int64)

    def print(self):
        border = list(self.border)
        for y in range(self.range_max[1], self.range_min[1] - 1, -1):
            txt = ""
            for x in range(self.range_min[0], self.range_max[0] + 1):
                coord = np.array([x, y])
                present = any(np.array_equal(coord, el) for el in border)
                txt += "#" if present else "."
            print(txt)
        print()

    def get_surface(self) -> int:
        """Get the total surface of the defined border.

        The border itself is included too.

        We use the shoelace formula to compute the surface.
        (https://en.wikipedia.org/wiki/Shoelace_formula)
        """
        det_sum = 0  # Sum of determinants
        for i, vertex in enumerate(self.vertices):
            next_idx = (i + 1) % len(self.vertices)
            next_vertex = self.vertices[next_idx]
            new_det = vertex[0] * next_vertex[1] - next_vertex[0] * vertex[1]
            det_sum += new_det

        area = -1.0 * det_sum / 2.0
        # Shoelace theorem, but vertices are clockwise, so negate

        border_points = len(list(self.border))

        interior_points = area - 0.5 * border_points + 1

        return interior_points + border_points


def main():

    plan = DigPlan()

    with open("input.txt", "r") as fh:
        while line := fh.readline():
            plan.add_instruction(line)

    # plan.print()  # 52231 for part 1

    surface = plan.get_surface()
    print("Surface:", surface)


if __name__ == "__main__":
    main()
