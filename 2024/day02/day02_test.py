# Unit tests for src/day02.py

import unittest
from argparse import Namespace

from day02 import main

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day02.test.dat')

class TestDay02(unittest.TestCase):

    def test_part_1(self):
        args = Namespace(file = test_data, part = 1, verbose = False)
        self.assertEqual(main(args), 2)

    def test_part_2(self):
        args = Namespace(file = test_data, part = 2, verbose = False)
        self.assertEqual(main(args), 4)

if __name__ == '__main__':
    unittest.main()





