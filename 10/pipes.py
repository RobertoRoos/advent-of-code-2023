from typing import Optional, Set, Dict, Tuple, List
from enum import Enum


Coord = Tuple[int, int]  # (row, column)


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = -1
    LEFT = -2


def flip(direction: Direction) -> Direction:
    return Direction(-direction.value)


class Tile:
    """Instantiate for a single tile in the maze.

    Coordinates are considered as (row, column), 0-indexed.
    """

    # Tiles by coordinates
    MAZE: Dict[Coord, "Tile"] = {}
    ROWS: int = 0
    COLS: int = 0

    def __init__(self, row: int, col: int, shape: str):
        self.row = row
        self.col = col
        self.shape = shape

        self.ports: Set[Direction] = set()

        if shape == "|":
            self.ports = (Direction.UP, Direction.DOWN)
        elif shape == "-":
            self.ports = (Direction.LEFT, Direction.RIGHT)
        elif shape == "L":
            self.ports = (Direction.UP, Direction.RIGHT)
        elif shape == "J":
            self.ports = (Direction.LEFT, Direction.UP)
        elif shape == "7":
            self.ports = (Direction.LEFT, Direction.DOWN)
        elif shape == "F":
            self.ports = (Direction.RIGHT, Direction.DOWN)
        elif shape == ".":
            pass
        elif shape == "S":
            self.ports = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
        else:
            raise ValueError(f"Unrecognized shape `{shape}`")

        self.add_to_maze(self)

    @classmethod
    def add_to_maze(cls, tile):
        row, col = tile.coordinates
        if row + 1 > cls.ROWS:
            cls.ROWS = row + 1
        if col + 1 > cls.COLS:
            cls.COLS = col + 1
        cls.MAZE[tile.coordinates] = tile

    def __repr__(self) -> str:
        return f"<Tile ({self.row},{self.col}), '{self.shape}'>"

    def get_neighbour(self, direction: Direction) -> Optional["Tile"]:
        coords = self.coordinates
        if direction == Direction.UP:
            coords = (coords[0] - 1, coords[1])
        elif direction == Direction.RIGHT:
            coords = (coords[0], coords[1] + 1)
        elif direction == Direction.DOWN:
            coords = (coords[0] + 1, coords[1])
        elif direction == Direction.LEFT:
            coords = (coords[0], coords[1] - 1)

        try:
            neighbour = self.MAZE[coords]
        except KeyError:
            return None

        if flip(direction) not in neighbour.ports:
            # Other tile does not connect back, not a valid neighbour
            return None

        return neighbour

    @property
    def coordinates(self) -> Coord:
        return self.row, self.col

    @classmethod
    def get_loop(cls, tile: "Tile") -> List["Tile"]:
        """Find the loop from a given tile.

        Splits (i.e. choices) cannot be present!

        :param tile: Starting tile
        """
        chain = [tile]

        # Find a starting direction:
        for first_direction in tile.ports:
            next_tile = tile.get_neighbour(first_direction)
            if next_tile is None:
                continue  # Direction is not valid

            tile = next_tile

            while tile is not None:
                chain.append(tile)
                tile = Tile.get_next(chain)

                if tile == chain[0]:
                    return chain  # Completed the chain!

        raise RuntimeError("Failed to close chain")

    @classmethod
    def get_next(cls, chain: List["Tile"]) -> "Tile":
        """Return next tile in a sequence."""
        for direction in chain[-1].ports:
            next_tile = chain[-1].get_neighbour(direction)
            if len(chain) > 1 and next_tile == chain[-2]:
                continue

            return next_tile

        raise RuntimeError(f"Could not find next in sequence")

    @classmethod
    def get_enclosed_count(cls, loop: List["Tile"]) -> int:
        """Get number of tiles fully enclosed by given loop."""
        loop_by_coordinates: Dict[Coord, Tile] = {tile.coordinates: tile for tile in loop}

        count = 0  # Number of surrounded tiles

        row_start = cls.ROWS - 1
        col_start = 0

        # Walk over all diagonals, from the bottom left to top right:
        while col_start < cls.COLS:
            col = col_start
            row = row_start

            inside = False  # Always start outside area

            while row < cls.ROWS and col < cls.COLS:

                tile = loop_by_coordinates.get((row, col), None)
                if tile is not None:
                    if (Direction.LEFT in tile.ports and Direction.DOWN in tile.ports or
                            Direction.UP in tile.ports and Direction.RIGHT in tile.ports):
                        pass  # Hit an empty corner, remain inside or outside
                    else:
                        inside = not inside  # Flip inside / outside state
                else:
                    if inside:
                        count += 1

                row += 1
                col += 1

            if row_start > 0:
                row_start -= 1
            else:
                col_start += 1

        # Scanning over diagonals is odd, but it saves us from awkward cases when scanning horizontal or vertical
        # when the scan follows the perimeter

        return count

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


def main():
    starting_tile: Optional[Tile] = None

    with open("input.txt", "r") as fh:
        row = 0
        while line := fh.readline():
            for col, shape in enumerate(line.strip()):
                new_tile = Tile(row, col, shape)
                if new_tile.shape == "S":
                    starting_tile = new_tile
            row += 1

    loop = Tile.get_loop(starting_tile)

    max_steps = int(len(loop) / 2)

    print(f"Biggest distance: {max_steps}")

    size = Tile.get_enclosed_count(loop)

    print(f"Enclosed tiles: {size}")


if __name__ == "__main__":
    main()
