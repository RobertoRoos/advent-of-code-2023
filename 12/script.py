from enum import Enum
from typing import Tuple, List, Union


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


def check_and_shorten_arrangement(
    states: StatesList, numbers: List[int]
) -> Union[None, Tuple[List[State], List[int]]]:
    """Remove starts of states and numbers that are known and match.

    Returns `None` if it doesn't match at all.
    """
    count = 0  # Consecutive broken ones
    idx_numbers = 0  # Index in `numbers`
    idx_broken_start = 0  # Index in `states` of the start of a broken sequence
    for i, state in enumerate(states):
        if state == State.UNKNOWN:
            break

        if state == State.BROKEN:
            if count == 0:
                idx_broken_start = i
            count += 1
        if state == State.OPERATIONAL or i == len(states) - 1:
            if count > 0:
                if idx_numbers >= len(numbers) or count != numbers[idx_numbers]:
                    return None  # Already not matching, abort this three
                idx_numbers += 1
                count = 0
            idx_broken_start = i + 1

    new_states, new_numbers = states[idx_broken_start:], numbers[idx_numbers:]

    if len(new_states) < sum(new_numbers) + len(new_numbers) - 1:
        return None  # No way we could still fit a valid sequence in here

    return new_states, new_numbers  # Could well be empty


def get_number_of_arrangements_recursively(
    states: StatesList, numbers: List[int]
) -> int:
    """Substitute remaining unknowns in `states` to find possible configurations."""
    arrangements = 0

    result = check_and_shorten_arrangement(states, numbers)
    if result is None:
        return arrangements  # Abort this tree, it already doesn't work

    new_states, new_numbers = result

    # Find the first unknown state:
    try:
        idx = next(i for i, s in enumerate(new_states) if s == State.UNKNOWN)
    except StopIteration:
        return 1  # No wildcards left, only one option left
    else:
        for option in (State.OPERATIONAL, State.BROKEN):
            new_states[idx] = option  # No need to copy, as `check_...()` does that
            arrangements += get_number_of_arrangements_recursively(
                new_states, new_numbers
            )

    return arrangements


def main():

    total_arrangements = 0

    part_2 = True

    with open("input_example.txt", "r") as fh:
        lines = 0
        while line := fh.readline():
            states_str, _, numbers_str = line.strip().partition(" ")

            if part_2:
                states_str = "?".join([states_str] * 5)
                numbers_str = ",".join([numbers_str] * 5)

            states = State.get_from_str(states_str)
            numbers = [int(s) for s in numbers_str.split(",")]
            arrangements = get_number_of_arrangements_recursively(states, numbers)
            total_arrangements += arrangements
            lines += 1

    print("Total:", total_arrangements)  # Works, but actually too slow


if __name__ == "__main__":
    main()
