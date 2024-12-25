from typing import Dict, Optional, List, Set
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
    def make_new(cls) -> "PartRange":
        return cls(ratings={c: set(range(1, 4_000 + 1)) for c in Category})

    def add(self, other_range: "PartRange"):
        """Include another range into this."""
        for c, r in other_range.ratings:
            if c in self.ratings:
                self.ratings[c] = self.ratings[c].union(r)
            else:
                self.ratings[c] = r


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

    def match(self, part: Part) -> bool:
        if self.category is None:
            return True  # Final clause

        part_value = part.ratings[self.category]
        if self.compare == ">":
            return part_value > self.threshold
        return part_value < self.threshold


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

    def get_previous(self, part_range) -> Dict[str, PartRange]:
        """Take a range of possible parts and split it backwards to previous workflows.

        :return: Names of the workflows before and their possible ranges.
        """
        return {}

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

    @classmethod
    def process_reverse(
        cls,
        heads: List[str],
        workflows_part_ranges: Optional[Dict[str, PartRange]] = None,
    ):
        """Track the possible ratings to get accepted.

        Uses recursion to walk back.
        """
        if workflows_part_ranges is None:
            workflows_part_ranges = {h: PartRange.make_new() for h in heads}

        new_heads = []

        for workflow_name in heads:
            workflow = Workflow.book[workflow_name]
            this_ranges = workflows_part_ranges[workflow_name]
            new_workflow_part_ranges = workflow.get_previous(this_ranges)
            for next_name, next_ranges in new_workflow_part_ranges.items():
                if next_name not in workflows_part_ranges:
                    workflows_part_ranges[next_name] = next_ranges
                else:
                    workflows_part_ranges[next_name].add(next_ranges)
                new_heads.append(next_name)

        if new_heads:
            cls.process_reverse(new_heads, workflows_part_ranges)
        else:
            return workflows_part_ranges["in"]


def main():

    # Add accepted and rejected as workflows:
    Workflow.book["A"] = Workflow(name="A", rules=[])
    Workflow.book["R"] = Workflow(name="R", rules=[])

    parts: List[Part] = []

    with open("input_example.txt", "r") as fh:
        while line := fh.readline():
            # Workflows
            if not line.strip():
                break

            Workflow.parse(line)

        while line := fh.readline():
            # Parts
            part = Part.parse(line)
            parts.append(part)

    # value = 0
    #
    # for part in parts:
    #     if Workflow.process(part):
    #         value += part.rating_sum
    #
    # print("Score:", value)  # 368964

    ranges = Workflow.process_reverse(heads=["A"])

    return


if __name__ == "__main__":
    main()
