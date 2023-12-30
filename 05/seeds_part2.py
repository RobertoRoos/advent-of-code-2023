from collections import OrderedDict
from typing import List, Dict, Tuple, Optional


class Mapping:
    """Contains a range of source-to-destination mapping."""

    def __init__(self, dst_start: int, src_start: int, length: int):
        if src_start < 0 or dst_start < 0 or length <= 0:
            raise ValueError(
                f"Values of {dst_start}, {src_start}, {length} are not valid!"
            )

        self.src_start = src_start
        self.dst_start = dst_start
        self.length = length

    def __repr__(self):
        return f"{self.dst_start} {self.src_start} {self.length}"

    @property
    def src_end(self) -> int:
        """Last src (inclusive)."""
        return self.src_start + self.length - 1

    @property
    def dst_end(self) -> int:
        """Last dst (inclusive)."""
        return self.dst_start + self.length - 1

    @staticmethod
    def from_string(line: str) -> "Mapping":
        numbers = [int(s) for s in line.strip().split()]
        return Mapping(*numbers)

    def parse(self, src: int) -> int:
        """Put a given src value through this mapping."""
        if src < self.src_start or src > self.src_end:
            raise ValueError(f"Given src {src} is outside this mapping range")

        return self.dst_start + (src - self.src_start)


class Range:
    """Contains a single range of values."""

    def __init__(
        self, start: int, length: Optional[int] = None, end: Optional[int] = None
    ):
        """

        Provide either `end` or `length` - both are inclusive!
        """
        if end is not None:
            length = end - start + 1

        if length is None or start < 0 or length <= 0:
            raise ValueError(f"Invalid range: {start}, {length}")

        self.start = start
        self.length = length

    def __repr__(self):
        return f"{self.start} {self.length}"

    @property
    def end(self):
        """Last value (inclusive)."""
        return self.start + self.length - 1

    def apply_list(self, mappings: List[Mapping]) -> List["Range"]:
        """Apply a list of other mappings to this one: this `dst` goes in as `src` for the other mappings.

        Also handle original mapping ranges that are untouched are returned as mappings.
        """
        current_ranges: List["Range"] = [self]
        new_ranges = []

        for mapping in mappings:
            i = 0
            while i < len(current_ranges):
                current_range = current_ranges[i]

                if (
                    mapping.src_end < current_range.start
                    or mapping.src_start > current_range.end
                ):
                    i += 1
                    continue  # No overlap at all

                current_ranges.pop(i)  # Remove this mapping from the current layer

                overlap_src_start = max(mapping.src_start, current_range.start)
                overlap_src_end = min(mapping.src_end, current_range.end)

                new_range = Range(
                    start=mapping.parse(overlap_src_start),
                    end=mapping.parse(overlap_src_end),
                )
                new_ranges.append(new_range)

                if overlap_src_start > current_range.start:
                    # We have original mapping preceding the overlap:
                    new_range = Range(
                        start=current_range.start,
                        end=overlap_src_start - 1,
                    )
                    current_ranges.append(new_range)

                if (length := current_range.end - overlap_src_end) > 0:
                    # We have original mapping after the overlap:
                    start = current_range.end - length + 1
                    new_range = Range(start=start, end=current_range.end)
                    current_ranges.append(new_range)

        return current_ranges + new_ranges


def main():
    # --- Parse input ---

    # Keep track of source-to-destination mappings:
    seed_ranges: List[Range] = []
    mappings_per_stage: OrderedDict[str, List[Mapping]] = OrderedDict()

    with open("input.txt", "r") as fh:
        line = fh.readline()
        seeds = [int(s) for s in line.partition(":")[2].split()]

        for i in range(0, len(seeds) - 1, 2):
            seed_ranges.append(Range(seeds[i], seeds[i + 1]))

        while (line := fh.readline()) != "":
            if line.strip() == "":
                title = fh.readline().partition(" ")[0]  # Next line contains title
                mappings_per_stage[title] = []
                continue  # Skip rest of outer loop

            new_map = Mapping.from_string(line)
            mappings_per_stage[title].append(new_map)

    # --- Parse input ---

    seed_ranges_before = seed_ranges

    for title, mappings in mappings_per_stage.items():
        print("Parsing: " + title)

        seed_ranges_after = []

        for seed_ranges_before_i in seed_ranges_before:
            seed_ranges_after += seed_ranges_before_i.apply_list(mappings)

        seed_ranges_before = seed_ranges_after

    start_numbers = [r.start for r in seed_ranges_before]

    print("Lowest location number:", min(start_numbers))

    return


if __name__ == "__main__":
    main()
