from typing import List, Tuple, Dict
from collections import namedtuple
from enum import IntEnum


class HandType(IntEnum):
    """Possible hands to get, sorted by value."""

    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


CardOccurrence = namedtuple("CardOccurrence", ["card", "count"])


class Hand:
    """Class for a set of 5 cards."""

    JOKERS = False

    CARDS = {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, txt: str):
        """

        :param txt: Five characters for this hand.
        """
        if len(txt) != 5:
            raise ValueError(f"Passed string `{txt}` is not 5 cards!")

        self.cards_str = txt

        # Cards in hand, in original order
        self.cards = [self.CARDS[c] for c in txt]

        self.hand_type = self.get_hand_type()

        return

    def __str__(self):
        return self.cards_str

    def __repr__(self):
        return f"<Hand instance `{self.__str__()}`>"

    def get_hand_type(self) -> HandType:
        """Find hand set for given hand."""

        card_counts = self.get_card_occurrences(self.cards)

        if self.JOKERS:
            i = 0
            while i < len(card_counts):
                if card_counts[i].card == 1 and len(card_counts) > 1:  # = "J"
                    # For a joker, add its count to the highest set instead:
                    idx = 0 if i > 0 else 1
                    new_count = card_counts[idx].count + card_counts[i].count
                    card_counts[idx] = card_counts[idx]._replace(count=new_count)
                    card_counts.pop(i)
                else:
                    i += 1

                continue

        if card_counts[0].count == 5:
            return HandType.FIVE_OF_A_KIND

        if card_counts[0].count == 4:
            return HandType.FOUR_OF_A_KIND

        if card_counts[0].count == 3 and card_counts[1].count == 2:
            return HandType.FULL_HOUSE

        if card_counts[0].count == 3:
            return HandType.THREE_OF_A_KIND

        if card_counts[0].count == 2 and card_counts[1].count == 2:
            return HandType.TWO_PAIR

        if card_counts[0].count == 2:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    @staticmethod
    def get_card_occurrences(cards: List[int]) -> List[CardOccurrence]:
        """Get list of card occurrence count, sorted descending.

        First value is card, second is occurrence.
        """

        # `Card: number of occurrences`
        card_counts: Dict[int, int] = {}

        for card in cards:
            if card not in card_counts:
                card_counts[card] = 0

            card_counts[card] += 1

        return [
            CardOccurrence(k, v)
            for k, v in sorted(card_counts.items(), key=lambda x: x[1], reverse=True)
        ]

    def __lt__(self, other: "Hand"):
        """Overload comparison operator.

        :return: True if `self` is less than `other`
        """
        if self.hand_type < other.hand_type:
            return True
        if self.hand_type > other.hand_type:
            return False

        # Hands are of equal type...

        for card_self, card_other in zip(self.cards, other.cards):
            if card_self < card_other:
                return True
            if card_self > card_other:
                return False

        raise ValueError(f"Cards `{self}` and `{other}` are the same!")


for _i in range(2, 10):
    Hand.CARDS[str(_i)] = _i


def main():
    Hand.JOKERS = True

    if Hand.JOKERS:
        Hand.CARDS["J"] = 1  # Lowest instead!

    hands_and_bids: List[Tuple[Hand, int]] = []

    with open("input.txt", "r") as fh:
        while (line := fh.readline()) != "":
            hand_str, _, bid_str = line.strip().partition(" ")

            hands_and_bids.append((Hand(hand_str), int(bid_str)))

    # Sort list of tuples by hand (weakest first)
    hands_and_bids_sorted = [
        (hand, bid) for hand, bid in sorted(hands_and_bids, key=lambda x: x[0])
    ]

    score = 0

    for i, hand_and_bid in enumerate(hands_and_bids_sorted):
        rank = i + 1
        score += rank * hand_and_bid[1]

    print("Final score is:", score)


if __name__ == "__main__":
    main()
