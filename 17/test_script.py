import unittest

from script import Map, Coord, State, PathInfo, Direction


class Day17TestCase(unittest.TestCase):

    def setUp(self):

        Map.STRAIGHT_MIN = 0
        Map.STRAIGHT_MAX = 3

        self.map = Map()
        for i in range(6):
            self.map.add_row("123456")

    def test_next_coord_corner(self):
        next_tiles = list(
            self.map.get_next_coords(
                State(
                    cost=0,
                    coord=Coord(0, 0),
                    info=PathInfo(straight_steps=0, direction=None),
                )
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(0, 1), Coord(1, 0)}, next_coords)
        next_steps = list(tile.info.straight_steps for tile in next_tiles)
        self.assertEqual([1, 1], next_steps)
        # The first tile is not counted as going straight

    def test_next_coord_middle(self):
        next_tiles = self.map.get_next_coords(
            State(
                cost=0,
                coord=Coord(2, 2),
                info=PathInfo(straight_steps=0, direction=Direction.SOUTH),
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(2, 3), Coord(2, 1), Coord(3, 2)}, next_coords)

    def test_next_coord_straight(self):
        next_tiles = self.map.get_next_coords(
            State(
                cost=0,
                coord=Coord(3, 3),
                info=PathInfo(straight_steps=3, direction=Direction.EAST),
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


class Day17TestCasePart2(unittest.TestCase):

    def setUp(self):

        Map.STRAIGHT_MIN = 4
        Map.STRAIGHT_MAX = 10

        self.map = Map()
        self.map.add_row("111111111111")
        self.map.add_row("999999999991")
        self.map.add_row("999999999991")
        self.map.add_row("999999999991")
        self.map.add_row("999999999991")
        # ^ provided example

    def test_next_coord_corner(self):
        next_tiles = list(
            self.map.get_next_coords(
                State(
                    cost=0,
                    coord=Coord(0, 0),
                    info=PathInfo(straight_steps=0, direction=None),
                )
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(0, 1), Coord(1, 0)}, next_coords)
        next_steps = list(tile.info.straight_steps for tile in next_tiles)
        self.assertEqual([1, 1], next_steps)
        # The first tile is not counted as going straight

    def test_next_coord_edge_minimum(self):
        next_tiles = list(
            self.map.get_next_coords(
                State(
                    cost=0,
                    coord=Coord(0, 3),
                    info=PathInfo(straight_steps=3, direction=Direction.EAST),
                )
            )
        )
        next_coords = set(tile.coord for tile in next_tiles)
        self.assertEqual({Coord(0, 4)}, next_coords)  # Couldn't go down
        next_steps = list(tile.info.straight_steps for tile in next_tiles)
        self.assertEqual([4], next_steps)

    def test_calculate_path(self):
        value = self.map.calculate_path()
        self.assertEqual(71, value)


if __name__ == "__main__":
    unittest.main()
