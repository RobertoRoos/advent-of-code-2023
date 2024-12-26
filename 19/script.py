from typing import Dict, Optional, List, Set, Tuple, Generator
from dataclasses import dataclass
from enum import Enum


class Category(Enum):
    COOL = "x"
    Musical = "m"
    AERODYNAMIC = "a"
    SHINY = "s"


@dataclass
class Part:
    """A single part item."""

    ratings: Dict[Category, int]

    @classmethod
    def parse(cls, line: str) -> "Part":
        line = line.strip().lstrip("{").rstrip("}")
        ratings = {}
        for prop in line.split(","):
            cat, _, rating = prop.partition("=")
            ratings[Category(cat)] = int(rating)

        return cls(ratings)

    @property
    def rating_sum(self) -> int:
        return sum(v for v in self.ratings.values())


@dataclass
class PartRange:
    """A range of parts, with multiple possible rating values."""

    ratings: Dict[Category, Set[int]]

    @classmethod
    def new_all(cls) -> "PartRange":
        return cls(ratings={c: set(range(1, 4_000 + 1)) for c in Category})

    @classmethod
    def new_none(cls) -> "PartRange":
        return cls(ratings={c: set() for c in Category})

    def add(self, other_range: "PartRange"):
        """Include another range into this."""
        for c, r in other_range.ratings.items():
            if c in self.ratings:
                self.ratings[c] = self.ratings[c].union(r)
            else:
                self.ratings[c] = r

    @property
    def count(self) -> int:
        p = 1
        for v in self.ratings.values():
            p *= len(v)
        return p


@dataclass
class Rule:
    """A rule of multiple in a workflow."""

    next_workflow_name: str
    category: Optional[Category] = None
    compare: Optional[str] = None
    threshold: Optional[int] = None

    @classmethod
    def from_string(cls, txt: str) -> "Rule":
        left, _, name = txt.rpartition(":")
        rule = Rule(next_workflow_name=name)
        if left:
            rule.category = Category(left[0])
            rule.compare = left[1]
            rule.threshold = int(left[2:])

        return rule

    def do_compare(self, value: int) -> bool:
        if self.compare == ">":
            return value > self.threshold
        if self.compare == "<":
            return value < self.threshold
        raise ValueError(f"Unrecognized symbol: {self.compare}")

    def match(self, part: Part) -> bool:
        if self.category is None:
            return True  # Final clause ("else")

        return self.do_compare(part.ratings[self.category])

    def split_range(self, part_range: PartRange) -> Tuple[PartRange, PartRange]:
        """

        :return: Range that matches this rule and then the range that remains.
        """
        if self.category is None:  # Final "else" clause
            return part_range, PartRange.new_none()

        range_match = PartRange.new_none()
        range_not_match = PartRange.new_none()
        for c, values in part_range.ratings.items():
            if c != self.category:
                range_match.ratings[c] = (
                    values  # Don't split the values of other categories
                )
                range_not_match.ratings[c] = values
        for v in part_range.ratings[self.category]:
            if self.do_compare(v):
                range_match.ratings[self.category].add(v)
            else:
                range_not_match.ratings[self.category].add(v)

        return range_match, range_not_match


class Workflow:
    """A single workflow instance."""

    # Lookup of all made workflows
    book: Dict[str, "Workflow"] = {}

    def __init__(self, name: str, rules: List[Rule]):
        self.name = name
        self.rules = rules

    @classmethod
    def parse(cls, line: str):
        """Register a new workflow."""
        name, _, rules_str = line.strip().partition("{")
        rules_str = rules_str.rstrip("}")
        rules = [Rule.from_string(s) for s in rules_str.split(",")]
        workflow = cls(name, rules)
        cls.book[name] = workflow

    def get_next(self, part: Part) -> str:
        """Parse a part through the rules, finding the next workflow."""
        for rule in self.rules:
            if rule.match(part):
                return rule.next_workflow_name

        raise ValueError("Not a single rule matched")

    @classmethod
    def process(cls, part: Part) -> bool:
        """True for accepted, False otherwise."""
        next_workflow_name = "in"
        while next_workflow_name:
            workflow = cls.book[next_workflow_name]
            next_workflow_name = workflow.get_next(part)

            if next_workflow_name == "A":
                return True
            elif next_workflow_name == "R":
                return False

    def get_next_ranges(
        self, part_range: PartRange
    ) -> Generator[Tuple[str, PartRange], None, None]:
        """Process a part range, splitting them over the next workflows."""
        part_range_not_match = part_range
        for rule in self.rules:
            part_range_match, part_range_not_match = rule.split_range(
                part_range_not_match
            )
            yield rule.next_workflow_name, part_range_match

    def process_range(self, part_range: PartRange) -> int:
        """Put a range of parts through the book and get the number of accepted values.

        We can check only the number of paths because none of the paths overlap, no need
        to union the set of ranges.

        Workflows are handled through recursion.
        """
        if self.name == "A":
            return part_range.count
        if self.name == "R":
            return 0

        final_part_range = 0

        for next_name, next_range in self.get_next_ranges(part_range):
            next_workflow = self.book[next_name]
            new_part_range = next_workflow.process_range(next_range)
            final_part_range += new_part_range

        return final_part_range

    def __repr__(self) -> str:
        return f"<Workflow '{self.name}'>"


def main():

    # Add accepted and rejected as workflows:
    Workflow.book["A"] = Workflow(name="A", rules=[])
    Workflow.book["R"] = Workflow(name="R", rules=[])

    parts: List[Part] = []

    with open("input.txt", "r") as fh:
        while line := fh.readline():
            # Workflows
            if not line.strip():
                break

            Workflow.parse(line)

        while line := fh.readline():
            # Parts
            part = Part.parse(line)
            parts.append(part)

    all_parts = PartRange.new_all()
    final_count = Workflow.book["in"].process_range(all_parts)

    print(f"Count: {final_count:,} ({final_count})")


if __name__ == "__main__":
    main()
