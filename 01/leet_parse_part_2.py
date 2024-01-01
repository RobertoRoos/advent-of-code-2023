from typing import Dict


number_words = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def get_numbers_in_string(line: str) -> Dict[int, str]:
    """Return `pos: number` dict of numbers."""

    numbers = {}

    for pos in range(len(line)):
        if (c := line[pos]).isdigit():
            numbers[pos] = c

    return numbers


def get_number_words_in_string(line: str) -> Dict[int, str]:
    """Return `pos: number` dict of numbers."""

    numbers = {}

    for i, word in enumerate(number_words):
        number = i + 1

        pos = 0
        while (pos := line.find(word, pos)) >= 0:
            numbers[pos] = str(number)
            pos += 1  # Increment pas found character

    return numbers


def main():
    with open("input.txt", "r") as fh:
        final_sum = 0

        for line in fh.readlines():
            numbers = get_numbers_in_string(line) | get_number_words_in_string(line)

            if len(numbers) < 1:
                raise ValueError(f"Line {line} does not seem to have numbers!")

            sorted_tuples = sorted(numbers.items(), key=lambda x: x[0])

            numbers = [p[1] for p in sorted_tuples]

            # Repeat the first digit if there is only one:
            number_str = numbers[0] + numbers[-1]

            number = int(number_str)
            final_sum += number

        print("Final sum:", final_sum)


if __name__ == "__main__":
    main()
