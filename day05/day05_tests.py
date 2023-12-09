# Unit tests for src/day05.py

import unittest
import numpy as np
from argparse import Namespace

from day05 import *

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day05.test.dat')
full_data = os.path.join(here, 'day05.dat')

class TestDay05(unittest.TestCase):

    def test_intersect(self):

        interval = (1, 9)
        breaks = np.array(5)
        self.assertEqual(intersect(interval, breaks, True), [(1, 4), (5, 9)])
        self.assertEqual(intersect(interval, breaks, False), [(1, 5), (6, 9)])

        breaks = np.array([3,6])
        self.assertEqual(intersect(interval, breaks, True), [(1, 2), (3, 5), (6, 9)])
        self.assertEqual(intersect(interval, breaks, False), [(1, 3), (4, 6), (7, 9)])

    def test_map_numbers(self):

        numbers = np.arange(0,10)

        # Identity map (src, tgt, tgt_start = src_start, rng_len)
        rule = Rule('foo', 'bar', np.array([3,6]), np.array([3,6]), np.array([2,2]))
        self.assertEqual(list(map_numbers(rule, numbers)), list(numbers))

        rule = Rule('foo', 'bar', np.array([0,5]), np.array([5,0]), np.array([5,5]))
        mapped = np.roll(numbers,5)
        self.assertEqual(list(map_numbers(rule, numbers)), list(mapped))

        numbers = np.arange(0,100)
        rule = Rule('seed', 'soil', np.array([50,52]), np.array([98,50]), np.array([2,48]))
        mapped = [(0, 49), (52, 99), (50, 51)]
        mapped = [np.arange(start, end + 1) for start, end in mapped]
        mapped = np.concatenate(mapped)
        self.assertEqual(list(map_numbers(rule, numbers)), list(mapped))

        # numbers = np.arange(69,74)
        # map = ('temp', 'hum', np.array([0,1]), np.array([69,0]), np.array([1,69]))
        # print(map_numbers(map, numbers))

    def test_intervals(self):

        interval = (0,9)

        # Identity map (src, tgt, tgt_start = src_start, rng_len)
        rule = Rule('foo', 'bar', np.array([3,6]), np.array([3,6]), np.array([2,2]))
        mapped = [(0,2), (3,4), (5,5), (6,7), (8,9)]
        self.assertEqual(map_intervals(rule, interval), mapped)

        rule = Rule('foo', 'bar', np.array([0,5]), np.array([5,0]), np.array([5,5]))
        mapped = [(5,9),(0,4)]
        self.assertEqual(map_intervals(rule, interval), mapped)

        interval = [(0,99)]
        rule = Rule('seed', 'soil', np.array([50,52]), np.array([50,52]), np.array([2,48]))
        mapped = [(0, 49), (50, 51), (52, 99)]
        self.assertEqual(map_intervals(rule, interval), mapped)

        # interval = [(69,73)]
        # map = ('temp', 'hum', np.array([0,1]), np.array([69,0]), np.array([1,69]))
        # print(map_intervals(map, interval))

    def test_part_1(self):
        args = Namespace(verbose=False, part=1, file=test_data, seeds=None)
        best = main(args)
        self.assertEqual(best, 35)

    def test_part_2(self):
        args = Namespace(verbose=False, part=2, file=test_data, seeds=None)
        best = main(args)
        self.assertEqual(best, 46)

if __name__ == '__main__':
    unittest.main()





