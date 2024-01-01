import numpy as np
import math


def get_number_of_options(time: int, distance: int) -> int:
    # The total traveled distance is:       `(tf - tb) * tb`
    # Because the final velocity equals the button press time, `tb`
    # Solving equating to the record time, quadratic formula:
    roots = np.roots([1, -time, distance])

    highest, lowest = (math.floor(max(roots)), math.ceil(min(roots)))
    return highest - lowest + 1


def main():
    with open("input.txt", "r") as fh:
        times_str = fh.readline()
        distances_str = fh.readline()

    times_str = times_str.partition(":")[2].strip()
    times = [int(k) for k in times_str.split()]

    distances_str = distances_str.partition(":")[2].strip()
    distances = [int(k) for k in distances_str.split()]

    # --- Part 1 ---

    running_product = 1

    for time, distance in zip(times, distances):
        number_of_options = get_number_of_options(time, distance)
        running_product *= number_of_options

    print("Final product:", running_product)

    # --- Part 2 ---

    super_time = int(times_str.replace(" ", ""))
    super_distance = int(distances_str.replace(" ", ""))

    number_of_options = get_number_of_options(super_time, super_distance)

    print("Number of super options:", number_of_options)


if __name__ == "__main__":
    main()
