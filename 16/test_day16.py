import unittest

from script import Direction, Contraption


class Day16TestCase(unittest.TestCase):
    def test_mirror(self):
        self.assertEqual(
            Direction.UP,
            Contraption.mirror(Direction.RIGHT, "/"),
        )
        self.assertEqual(
            Direction.DOWN,
            Contraption.mirror(Direction.RIGHT, "\\"),
        )
        self.assertEqual(
            Direction.UP,
            Contraption.mirror(Direction.LEFT, "\\"),
        )


if __name__ == "__main__":
    unittest.main()
