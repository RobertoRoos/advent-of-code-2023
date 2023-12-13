import re


def main():
    re_numbers = re.compile(r"[0-9]+")  # A single or more digits

    with open("input.txt", "r") as fh:
        lines = fh.readlines()

    part_sum = 0

    normal_chars = set("0123456789.\n")

    for idx, line in enumerate(lines):
        line_prev = lines[idx - 1] if idx > 0 else None
        line_next = lines[idx + 1] if idx < len(lines) - 1 else None

        for m in re_numbers.finditer(line):
            # Build a string for the block with one layer surrounding:
            block = ""
            pos_start = max(m.start() - 1, 0)  # Horizontal range of block
            pos_end = min(m.end() + 1, len(line))  # (Not inclusive!)

            for line_i in [line_prev, line, line_next]:
                if line_i is not None:
                    block += line_i[pos_start : pos_end]

            if not set(block) <= normal_chars:  # If all characters are of the whitelist
                val = int(m.group())
                part_sum += val

        pass

    print("Sum of part numbers:", part_sum)


if __name__ == "__main__":
    main()
