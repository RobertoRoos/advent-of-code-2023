from enum import Enum
from typing import Tuple, List, Union
from itertools import product


class State(Enum):
    """Hot spring state (with ascii symbol."""

    BROKEN = "#"
    OPERATIONAL = "."
    UNKNOWN = "?"

    @staticmethod
    def get_from_str(txt: str) -> List["State"]:
        """Parse a string into state instances."""
        return [State(c) for c in txt]


StatesList = Union[List[State], Tuple[State]]


# def get_arrangement_numbers(states: StatesList) -> List[int]:
#     """Take in a possible row of states and return the corresponding counts."""
#     numbers = []
#     count = 0
#     for i, state in enumerate(states):
#         if state == State.BROKEN:
#             count += 1  # Count consecutive broken ones
#
#         if count > 0 and (state != State.BROKEN or i == len(states) - 1):
#             numbers.append(count)
#             count = 0
#
#     return numbers


def check_arrangement_numbers(states: StatesList, numbers_check: List[int]) -> bool:
    """Check if a states arrangement fits a numbers list."""
    count = 0
    next_index = 0
    for i, state in enumerate(states):
        if state == State.BROKEN:
            count += 1  # Count consecutive broken ones

        if count > 0 and (state != State.BROKEN or i == len(states) - 1):
            if next_index >= len(numbers_check):
                return False  # Different amount of numbers, not a match

            if numbers_check[next_index] != count:
                return False  # Mismatch

            count = 0
            next_index += 1

    return len(numbers_check) == next_index


def get_arrangement_numbers(states: StatesList) -> List[int]:
    """Take in a possible row of states and return the corresponding counts."""
    numbers = []
    count = 0
    for i, state in enumerate(states):
        if state == State.BROKEN:
            count += 1  # Count consecutive broken ones

        if count > 0 and (state != State.BROKEN or i == len(states) - 1):
            numbers.append(count)
            count = 0

    return numbers


def get_number_of_arrangements(states: StatesList, numbers: List[int]) -> int:
    """Return the number of possible arrangement per line."""
    options = 0

    # Get indices of unknown entries:
    idx_unknown = [i for i, s in enumerate(states) if s == State.UNKNOWN]

    # Loop over all possible options for this list:
    for comb in product([State.BROKEN, State.OPERATIONAL], repeat=len(idx_unknown)):
        states_option = states[:]  # Deep copy
        for idx, new_state in zip(idx_unknown, comb):
            states_option[idx] = new_state
        if check_arrangement_numbers(states_option, numbers):
            options += 1

    if options == 0:
        raise RuntimeError("Number of options cannot be zero")

    return options


def main():

    total_arrangements = 0

    with open("input.txt", "r") as fh:
        lines = 0
        while line := fh.readline():
            states_str, _, numbers_str = line.partition(" ")
            states = State.get_from_str(states_str)
            numbers = [int(s) for s in numbers_str.split(",")]
            total_arrangements += get_number_of_arrangements(states, numbers)
            lines += 1

    print("Total:", total_arrangements)  # Works, but actually too slow


if __name__ == "__main__":
    main()
