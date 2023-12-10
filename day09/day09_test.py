# Unit tests for src/day09.py

import unittest
from argparse import Namespace

from day09 import *

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day09.test.dat')
full_data = os.path.join(here, 'day09.dat')

class TestDay09(unittest.TestCase):

    def test_parse_line(self):
        self.assertEqual(parse_line('0 3 6 9 12 15', 1, False), 18)
        self.assertEqual(parse_line('1 3 6 10 15 21', 1, False), 28)
        self.assertEqual(parse_line('10 13 16 21 30 45', 1, False), 68)
        self.assertEqual(parse_line('-3 -1 1 3', 1,False),5)

    def test_parse_line_2(self):
        self.assertEqual(parse_line('0 3 6 9 12 15', 2, False), -3)
        self.assertEqual(parse_line('1 3 6 10 15 21', 2, False), 0)
        self.assertEqual(parse_line('10 13 16 21 30 45', 2, False), 5)

    def test_part_1(self):
        args = Namespace(file = test_data, part = 1, verbose = False)
        self.assertEqual(main(args), 114)

    def test_part_1_full(self):
        args = Namespace(file = full_data, part = 1, verbose = False)
        self.assertEqual(main(args), 1757008019)

    def test_part_2(self):
        args = Namespace(file = test_data, part = 2, verbose = False)
        self.assertEqual(main(args), 2)

if __name__ == '__main__':
    unittest.main()





