import unittest

from script import (
    check_and_shorten_arrangement,
    get_number_of_arrangements_recursively,
    State,
)


class Day12TestCase(unittest.TestCase):

    def test_shorten(self):
        states = State.get_from_str(".#.#.??#.")
        states_expected = State.get_from_str("??#.")
        result = check_and_shorten_arrangement(states, [1, 1, 2])
        self.assertEqual(states_expected, result[0])
        self.assertEqual([2], result[1])

    def test_shorten_finished(self):
        states = State.get_from_str(".#.#")
        result = check_and_shorten_arrangement(states, [1, 1])
        self.assertEqual(([], []), result)

    def test_func(self):
        states = State.get_from_str(".??..??...?##.")
        arrangements = get_number_of_arrangements_recursively(states, [1, 1, 3])
        self.assertEqual(4, arrangements)

    def test_func_2(self):
        states = State.get_from_str("?###????????")
        arrangements = get_number_of_arrangements_recursively(states, [3, 2, 1])
        self.assertEqual(10, arrangements)

    def test_func_long(self):
        states_str = "?".join(["?###????????"] * 5)
        states = State.get_from_str(states_str)
        numbers = [3, 2, 1] * 5
        arrangements = get_number_of_arrangements_recursively(states, numbers)
        self.assertEqual(506250, arrangements)


if __name__ == "__main__":
    unittest.main()
