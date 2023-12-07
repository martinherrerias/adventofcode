# Unit tests for src/day06.py

import unittest
from argparse import Namespace

from day06 import *

class TestDay06(unittest.TestCase):

    def test_race(self):
        self.assertEqual(race(7, 9, True), 4)
        self.assertEqual(race(15, 40, True), 8)
        self.assertEqual(race(30, 200, True), 9)
        self.assertEqual(race(10, 25, True), 0)

    def test_part_1(self):
        args = Namespace(file = 'test_data/day06.txt', part = 1, verbose = False)
        best = main(args)
        self.assertEqual(best, 288)

        args = Namespace(file = 'data/day06.txt', part = 1, verbose = False)
        best = main(args)
        self.assertEqual(best, 114400)

    def test_part_2(self):
        args = Namespace(file = 'test_data/day06.txt', part = 2, verbose = False)
        best = main(args)
        self.assertEqual(best, 71503)

        args = Namespace(file = 'data/day06.txt', part = 2, verbose = False)
        best = main(args)
        self.assertEqual(best, 21039729)

if __name__ == '__main__':
    unittest.main()





