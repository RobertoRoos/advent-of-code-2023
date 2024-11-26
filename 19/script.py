from typing import Dict, Optional, List
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

    @classmethod
    def process_reverse(cls, workflows: Optional[List["Workflow"]] = None) -> int:
        """Count the number of parts that could be accepted by working backwards from all acceptations.

        Uses recursion to walk back.
        """
        count = 0
        if workflows is None:
            workflows = []
            for w in cls.book.values():
                if any(r.next_workflow_name == "A" for r in w.rules):
                    workflows.append(w)

        return count


def main():
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

    number_options = Workflow.process_reverse()

    return


if __name__ == "__main__":
    main()
