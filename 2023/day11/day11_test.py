# Unit tests for src/day11.py

import unittest
from argparse import Namespace

from day11 import *

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day11.test.dat')

class TestDay11(unittest.TestCase):

    def test_expand(self):
        self.assertEqual(expand([0,1,0]).tolist(), [0,1,3])
        self.assertEqual(expand([1,0,1]).tolist(), [0,2,3])
        self.assertEqual(expand([1,1,1]).tolist(), [0,1,2])

    def test_expand_scale(self):
        self.assertEqual(expand([0,1,0],3).tolist(), [0,1,4])
        self.assertEqual(expand([1,0,1],5).tolist(), [0,5,6])

    def test_dist(self):
        self.assertEqual( dist(1,6,5,11), 9)
        self.assertEqual( dist(4,0,9,10), 15)

    def test_part_1(self):
        args = Namespace(file = test_data, scale = 2, verbose = False)
        self.assertEqual(main(args), 374)

    def test_part_2(self):
        args = Namespace(file = test_data, scale = 10, verbose = False)
        self.assertEqual(main(args), 1030)
        args = Namespace(file = test_data, scale = 100, verbose = False)
        self.assertEqual(main(args), 8410)

if __name__ == '__main__':
    unittest.main()





