# Unit tests for src/day.py

import unittest
from argparse import Namespace

from day01 import main

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day01.test.dat')

class TestDay(unittest.TestCase):

    def test_part_1(self):
        args = Namespace(file = test_data, part = 1, verbose = False)
        self.assertEqual(main(args), 11)

    def test_part_2(self):
        args = Namespace(file = test_data, part = 2, verbose = False)
        self.assertEqual(main(args), 31)

if __name__ == '__main__':
    unittest.main()





