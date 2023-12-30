import numpy as np
import math


def main():
    with open("input.txt", "r") as fh:
        times_str = fh.readline()
        distances_str = fh.readline()

    times_str = times_str.partition(":")[2].strip()
    times = [int(k) for k in times_str.split()]

    distances_str = distances_str.partition(":")[2].strip()
    distances = [int(k) for k in distances_str.split()]

    running_product = 1

    for time, distance in zip(times, distances):

        # The total traveled distance is:       `(tf - tb) * tb`
        # Because the final velocity equals the button press time, `tb`
        # Solving equating to the record time, quadratic formula:
        roots = np.roots([1, -time, distance])

        highest, lowest = (math.floor(max(roots)), math.ceil(min(roots)))
        number_of_options = highest - lowest + 1

        running_product *= number_of_options

    print("Final product:", running_product)


if __name__ == '__main__':
    main()
