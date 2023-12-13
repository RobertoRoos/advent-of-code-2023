from typing import List
import re


def find_whole_numbers(line: str, pos: int) -> List[int]:
    """Given a position, return the whole numbers included in part, with a width of 1 around the position."""

    if line[pos].isdigit():
        # Grow left and right
        left = pos
        while left > 0 and line[left].isdigit():
            left -= 1

        right = pos
        while right < len(line) and line[right].isdigit():
            right += 1

        substr = line[left + 1 : right]  # Range is not inclusive!
        return [int(substr)]

    numbers = []

    if pos > 0 and line[pos - 1].isdigit():
        # Grow left
        left = pos - 1
        while left >= 0 and line[left].isdigit():
            left -= 1

        substr = line[left + 1 : pos]  # Range is not inclusive!
        numbers.append(int(substr))

    if pos < len(line) and line[pos + 1].isdigit():
        # Grow right
        right = pos + 1
        while right > 0 and line[right].isdigit():
            right += 1

        substr = line[pos + 1 : right]  # Range is not inclusive!
        numbers.append(int(substr))

    return numbers


def main():
    re_numbers = re.compile(r"[0-9]+")  # A single or more digits

    with open("input.txt", "r") as fh:
        lines = fh.readlines()

    part_sum = 0
    gear_ratio_sum = 0

    normal_chars = set("0123456789.\n")

    for idx, line in enumerate(lines):
        line_prev = lines[idx - 1] if idx > 0 else None
        line_next = lines[idx + 1] if idx < len(lines) - 1 else None

        # --- Get parts sum ---

        for m in re_numbers.finditer(line):
            # Build a string for the block with one layer surrounding:
            block = ""
            pos_start = max(m.start() - 1, 0)  # Horizontal range of block
            pos_end = min(m.end() + 1, len(line))  # (Not inclusive!)

            for line_i in [line_prev, line, line_next]:
                if line_i is not None:
                    block += line_i[pos_start:pos_end]

            if not set(block) <= normal_chars:  # If all characters are of the whitelist
                val = int(m.group())
                part_sum += val

        # --- Get gear ratio sum- --

        pos = 0
        while (pos := line.find("*", pos + 1)) >= 0:
            # Found an asterix at `pos`
            numbers = []

            for line_i in [line_prev, line, line_next]:
                if line_i is not None:
                    numbers += find_whole_numbers(line_i, pos)

            if len(numbers) == 2:
                gear_ratio_sum += numbers[0] * numbers[1]
            elif len(numbers) > 2:
                raise ValueError(f"More than two numbers found in line {idx}:{pos}")

    print("Sum of part numbers:", part_sum)

    print("Sum of gear products:", gear_ratio_sum)


if __name__ == "__main__":
    main()
