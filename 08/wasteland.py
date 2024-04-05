from typing import List, Optional, Dict


class Node:
    """Container for a node, contain a left and right sub-node."""

    ALL: Dict[str, "Node"] = {}  # "name": "node"

    def __init__(self, name: str, left_name: Optional[str] = None, right_name: Optional[str] = None):
        self.name = name
        self.left_name = left_name
        self.right_name = right_name

        self.ALL[self.name] = self

    @property
    def left(self) -> "Node":
        return self.get_or_make(self.left_name)

    @property
    def right(self) -> "Node":
        return self.get_or_make(self.right_name)

    def __repr__(self):
        return f"Node ({self.name})"

    @classmethod
    def get_or_make(cls, name: str) -> "Node":
        if name in cls.ALL:
            return cls.ALL[name]

        return Node(name)  # Registration is done inside constructor


def main():

    with (open("input.txt", "r") as fh):

        directions_str = fh.readline().strip()
        fh.readline()

        while (line := fh.readline()) != "":

            node_name, _, line_rest = line.partition("=")
            line_rest = line_rest.strip().lstrip("(").rstrip(")")
            left_name, _, right_name = line_rest.partition(",")
            node_name, left_name, right_name = node_name.strip(), left_name.strip(), right_name.strip()

            Node(node_name, left_name, right_name)  # No need to save reference to object

    current_node = Node.ALL["AAA"]
    directions_index = 0
    steps = 0

    while current_node.name != "ZZZ":
        if directions_str[directions_index] == "L":
            current_node = current_node.left
        else:
            current_node = current_node.right

        steps += 1
        directions_index += 1
        if directions_index >= len(directions_str):
            directions_index = 0

        if steps > 100000:
            raise RuntimeError("Steps getting too big, something is probably wrong")

    print(f"Total steps taken: {steps}")


if __name__ == "__main__":
    main()
