from typing import Set


def numbers_to_set(txt: str) -> Set[int]:
    txt = txt.strip()
    numbers = [int(s) for s in txt.split()]
    return set(numbers)


def main():
    total_points = 0

    with open("input.txt", "r") as fh:
        while (line := fh.readline()) != "":
            _, _, line_numbers = line.partition(":")
            numbers_left, _, numbers_right = line_numbers.partition("|")

            numbers_winning = numbers_to_set(numbers_left)
            numbers_card = numbers_to_set(numbers_right)

            wins = len(
                numbers_winning & numbers_card
            )  # Get length of the union of both sets

            if wins > 0:
                total_points += 2 ** (wins - 1)

    print("Total points worth:", total_points)


if __name__ == "__main__":
    main()
