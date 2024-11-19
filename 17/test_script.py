import unittest

from script import Map, Coord, State, CoordExtras, Direction


class Day17TestCase(unittest.TestCase):

    def setUp(self):
        self.map = Map()
        for i in range(6):
            self.map.add_row("123456")

    def test_next_coord_corner(self):
        next_tiles = list(
            self.map.get_next_coords(
                State(
                    cost=0,
                    coord=Coord(0, 0),
                    extras=CoordExtras(straight_steps=0, direction=None),
                )
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(0, 1), Coord(1, 0)}, next_coords)
        next_steps = list(tile.extras.straight_steps for tile in next_tiles)
        self.assertEqual([1, 1], next_steps)

    def test_next_coord_middle(self):
        next_tiles = self.map.get_next_coords(
            State(
                cost=0,
                coord=Coord(2, 2),
                extras=CoordExtras(straight_steps=0, direction=Direction.SOUTH),
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(2, 3), Coord(2, 1), Coord(3, 2)}, next_coords)

    def test_next_coord_straight(self):
        next_tiles = self.map.get_next_coords(
            State(
                cost=0,
                coord=Coord(3, 3),
                extras=CoordExtras(straight_steps=3, direction=Direction.EAST),
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(4, 3), Coord(2, 3)}, next_coords)

    def test_calculate_path_basic(self):
        my_map = Map()
        for i in range(5):
            my_map.add_row("11111")
        value = my_map.calculate_path()
        self.assertEqual(8, value)

    def test_calculate_path(self):
        value = self.map.calculate_path()
        self.assertEqual(28, value)


if __name__ == "__main__":
    unittest.main()
