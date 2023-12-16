from collections import defaultdict
from typing import List, Dict, Tuple


def main():
    # Keep track of each kind of mapping for each seed (so discarding intermediate
    # maps)
    seeds_to_dst: Dict[int, int]

    with open("input.txt", "r") as fh:
        line = fh.readline()
        seeds = [int(s) for s in line.partition(":")[2].split()]
        seeds_to_dst = {s: s for s in seeds}
        seeds_to_dst_new = dict(seeds_to_dst)

        while (line := fh.readline()) != "":
            if line.strip() == "":
                title = fh.readline().partition(" ")[0]  # Next line contains title
                print("Section:", title)
                seeds_to_dst = dict(seeds_to_dst_new)
                continue

            numbers = [int(s) for s in line.strip().split()]

            dst_start, src_start, length = numbers

            for seed, dst in seeds_to_dst.items():
                if src_start <= dst < src_start + length:
                    # If this key is in the source range:
                    seeds_to_dst_new[seed] = dst_start + dst - src_start
                    pass

            pass

        seeds_to_dst = dict(seeds_to_dst_new)

    lowest_location = min(seeds_to_dst.values())

    print("The lowest value for location is:", lowest_location)


if __name__ == "__main__":
    main()
