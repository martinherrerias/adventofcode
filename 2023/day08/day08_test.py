# Unit tests for src/day08.py

import unittest
from argparse import Namespace

from day08 import *

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = [os.path.join(here, f'day08{x}.test.dat') for x in 'abcd']
full_data = os.path.join(here, 'day08.dat')

class TestDay08(unittest.TestCase):

    def test_parse_node(self):
        self.assertEqual(parse_node('AAA = (BBB, CCC)'), Node('AAA', 'BBB', 'CCC'))

    def test_part_1a(self):
        args = Namespace(file = test_data[0], part = 1, verbose = True, debug = False, test = False)
        self.assertEqual(main(args), 2)

    def test_part_1b(self):
        args = Namespace(file = test_data[1], part = 1, verbose = True, debug = False, test = False)
        self.assertEqual(main(args), 6)

    def test_part_1c(self):
        # Same as part a but with nodes shuffled
        args = Namespace(file = test_data[2], part = 1, verbose = False, debug = False, test = False)
        self.assertEqual(main(args), 2)

    def test_part_1_full(self):
        args = Namespace(file = full_data, part = 1, verbose = False, debug = False, test = False)
        self.assertEqual(main(args), 22199)

    def test_part_2(self):
        args = Namespace(file = test_data[3], part = 2, verbose = True, debug = False, test = False)
        self.assertEqual(main(args), 6)

    @unittest.skip('Takes too long')
    def test_part_2_full(self):
        args = Namespace(file = full_data, part = 2, verbose = True, debug = False, test = False)
        self.assertEqual(main(args), 13334102464297)

if __name__ == '__main__':
    unittest.main()