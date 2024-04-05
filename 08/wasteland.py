from typing import Optional, Dict, List
from math import lcm


class Node:
    """Container for a node, contain a left and right sub-node."""

    ALL: Dict[str, "Node"] = {}  # "name": "node"

    def __init__(
        self,
        name: str,
        left_name: Optional[str] = None,
        right_name: Optional[str] = None,
    ):
        if name is None or len(name) != 3:
            raise ValueError("Name must be valid")

        if name in self.ALL:
            raise ValueError(f"Node `{name}` already registered!")

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
    with open("input.txt", "r") as fh:
        directions_str = fh.readline().strip()
        fh.readline()

        while (line := fh.readline()) != "":
            node_name, _, line_rest = line.partition("=")
            line_rest = line_rest.strip().lstrip("(").rstrip(")")
            left_name, _, right_name = line_rest.partition(",")
            node_name, left_name, right_name = (
                node_name.strip(),
                left_name.strip(),
                right_name.strip(),
            )

            Node(
                node_name, left_name, right_name
            )  # No need to save reference to object

    current_node_names = [name for name in Node.ALL.keys() if name.endswith("A")]
    directions_index = 0
    directions_len = len(directions_str)
    steps = 0

    node_last_steps_on_z: List[Optional[int]] = [None] * len(current_node_names)
    node_cycles: List[Optional[int]] = [None] * len(current_node_names)

    # Keep walking through all the nodes until we've figured out the repeating patter
    # for each starting node:

    while any(n is None for n in node_cycles):
        for i, current_node_name in enumerate(current_node_names):
            if directions_str[directions_index] == "L":
                current_node_names[i] = Node.ALL[current_node_name].left_name
            else:
                current_node_names[i] = Node.ALL[current_node_name].right_name

            if current_node_names[i].endswith("Z"):
                if node_cycles[i] is None:
                    if node_last_steps_on_z[i] is not None:
                        node_cycles[i] = steps - node_last_steps_on_z[i]
                    node_last_steps_on_z[i] = steps

        if steps > 10000000:
            print(f"Aborted after {steps} steps...")
            return
            # raise RuntimeError(f"Steps exceeded {steps}, something is probably wrong")

        steps += 1
        directions_index += 1
        if directions_index >= directions_len:
            directions_index = 0

    print(f"Found pattern after steps: {steps}")

    expected_steps = lcm(*node_cycles)
    print(f"Expect to get there after {expected_steps} steps")


if __name__ == "__main__":
    main()
