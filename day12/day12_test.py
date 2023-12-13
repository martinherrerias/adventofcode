# Unit tests for src/day12.py

import unittest
from argparse import Namespace

from day12 import *

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day12.test.dat')

class TestDay12(unittest.TestCase):

    def test_check_line(self):
        self.assertEqual(check_line('##.###.#', [2,3,1]), True)
        self.assertEqual(check_line('##.###.#', [2,2,1,1]), False)

    def test_parse_line(self):
        self.assertEqual(parse_line('???.### 1,1,3', 1), 1)
        self.assertEqual(parse_line('.??..??...?##. 1,1,3', 1), 4)
        self.assertEqual(parse_line('?###???????? 3,2,1', 1), 10)

    def test_parse_line_2(self):
        self.assertEqual(parse_line('???.### 1,1,3', 2, True), 1)
        self.assertEqual(parse_line('.??..??...?##. 1,1,3', 2, True), 16384)
        # self.assertEqual(parse_line('?###???????? 3,2,1', 1), 506250)

    @unittest.skip("Skipping part 2")
    def test_part_1(self):
        args = Namespace(file = test_data, part = 1, verbose = False)
        self.assertEqual(main(args), 21)
    
    @unittest.skip("Skipping part 2")
    def test_part_2(self):
        args = Namespace(file = test_data, part = 2, verbose = False)
        self.assertEqual(main(args), 525152)

if __name__ == '__main__':
    unittest.main()





