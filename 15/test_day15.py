import unittest

from script import hash_function


class Day15Tests(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(52, hash_function("HASH"))

    def test_hash_line(self):
        txt = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
        val = sum(hash_function(part) for part in txt.split(","))
        self.assertEqual(1320, val)


if __name__ == "__main__":
    unittest.main()
