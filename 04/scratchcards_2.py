from collections import defaultdict
from typing import Set, Dict


def numbers_to_set(txt: str) -> Set[int]:
    txt = txt.strip()
    numbers = [int(s) for s in txt.split()]
    return set(numbers)


def main():
    total_cards = 0

    # How many copies we encountered of a given card
    card_copies: Dict[int, int] = defaultdict(lambda: 1)  # Always at least one copy

    with open("input.txt", "r") as fh:
        while (line := fh.readline()) != "":
            card_str, _, line_numbers = line.partition(":")

            card = int(card_str[4:])

            card_count = card_copies[card]  # How many copies we have of this card

            total_cards += card_count

            numbers_left, _, numbers_right = line_numbers.partition("|")

            numbers_winning = numbers_to_set(numbers_left)
            numbers_card = numbers_to_set(numbers_right)

            wins = len(
                numbers_winning & numbers_card
            )  # Get length of the union of both sets

            if wins > 0:
                for next_card in range(card + 1, card + wins + 1):
                    card_copies[next_card] += card_count

    print("Total cards:", total_cards)


if __name__ == "__main__":
    main()
