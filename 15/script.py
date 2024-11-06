import re
from typing import List, NamedTuple
from collections import OrderedDict

from tornado.options import options


def hash_function(txt: str) -> int:
    """The HASH function."""
    value = 0
    for c in txt:
        value += ord(c)
        value *= 17
        value %= 256
    return value


class Lens(NamedTuple):
    label: str
    focal_length: int


def main():
    with open("input.txt", "r") as fh:
        line = fh.readline().strip()

    # Part 1:
    parts = line.split(",")
    value = sum(hash_function(part) for part in parts)

    print("Sum:", value)

    # Part 2:

    # Initialize all empty boxes:
    boxes: List[OrderedDict[str, int]] = [OrderedDict() for _ in range(256)]

    re_part = re.compile(r"(\w+)([=-])(\w+)?")

    for part in parts:
        groups = re_part.match(part).groups()
        label, operation = groups[0], groups[1]
        focal_length = groups[2] if len(groups) > 2 else None

        box_idx = hash_function(label)

        if operation == "=":
            boxes[box_idx][label] = int(focal_length)
        else:
            boxes[box_idx].pop(label, None)

    # Compute magic number:
    value = 0
    for box_idx, box in enumerate(boxes):
        for place, (label, focal_length) in enumerate(box.items()):
            new_val = (place + 1) * (box_idx + 1) * focal_length
            value += new_val

    print("Sum:", value)


if __name__ == "__main__":
    main()
