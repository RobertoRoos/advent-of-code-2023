import unittest

from script import Tile, find_horizontal_symmetry, rotate_pattern, get_score


class Day13TestCase(unittest.TestCase):

    def test_find_horizontal_symmetry(self):
        content = """
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        pattern = [Tile.get_list_from_text(l) for l in content.split()]
        row = find_horizontal_symmetry(pattern)
        self.assertEqual(4, row)

    def test_rotate_pattern(self):
        content = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        pattern = [Tile.get_list_from_text(l) for l in content.split()]
        new_pattern = rotate_pattern(pattern)
        self.assertEqual(7, len(pattern))
        self.assertEqual(9, len(pattern[0]))

    def test_get_score(self):
        content = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        pattern = [Tile.get_list_from_text(l) for l in content.split()]
        score = get_score(pattern)
        self.assertEqual(5, score)

    def test_get_score_smudge(self):
        content = """
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        pattern = [Tile.get_list_from_text(l) for l in content.split()]
        score = get_score(pattern, expected_errors=1)
        self.assertEqual(100, score)

    def test_get_score_smudge_2(self):
        content = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        pattern = [Tile.get_list_from_text(l) for l in content.split()]
        score = get_score(pattern, expected_errors=1)
        self.assertEqual(300, score)


if __name__ == "__main__":
    unittest.main()
