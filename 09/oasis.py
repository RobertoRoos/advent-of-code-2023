from typing import List


def get_next_in_sequence(initial_sequence: List[int]) -> int:
    """Compute the next value in the sequence based on the diff rules."""

    sequences_list: List[List[int]] = [initial_sequence]

    steps = 0

    last_sequence = sequences_list[-1]

    # Find next diff-list that is all zeroes:
    while any(number != 0 for number in last_sequence):
        next_sequence: List[int] = []
        for i in range(len(last_sequence) - 1):
            next_sequence.append(last_sequence[i + 1] - last_sequence[i])

        sequences_list.append(next_sequence)
        last_sequence = next_sequence

        steps += 1
        if steps > 100000:
            raise RuntimeError(f"Steps exceeding {steps}, halting")

    last_sequence.append(0)  # Add a new zero to the last row

    # Now work our way back up to find the next number of the initial sequence:
    for i in range(len(sequences_list) - 2, -1, -1):
        # Next value is the sum of the end of the seq. + the last value of the prev. seq.:
        new_val = sequences_list[i + 1][-1] + sequences_list[i][-1]
        sequences_list[i].append(new_val)

    return sequences_list[0][-1]  # Last new value


def main():
    new_sum = 0

    with open("input.txt", "r") as fh:
        while (line := fh.readline()) != "":
            sequence = [int(txt) for txt in line.strip().split()]

            next_value = get_next_in_sequence(sequence)

            new_sum += next_value

    print(f"Total sum of new values: {new_sum}")


if __name__ == "__main__":
    main()
