# Unit tests for src/day10.py

import unittest
from argparse import Namespace
import numpy as np

from day10 import *

import os
import glob
import re

here = os.path.dirname(os.path.realpath(__file__))
test_data = glob.glob(os.path.join(here, '*.test.dat'))
keys = [re.match(r'.*(\w).test.dat', f).group(1) for f in test_data]
test_data = dict(zip(keys, test_data))
full_data = os.path.join(here, 'day10.dat')

class TestDay10(unittest.TestCase):

    def test_connections(self):
        input = np.array([
            ['S', '-', '7'],
            ['|', '.', '|'],
            ['L', '-', 'J']
        ])
        tiles = [[get_tile(c) for c in line] for line in input]
        self.assertEqual(list(connections(tiles, 0, 0)), [(1,0), (0,1)])
        self.assertEqual(list(connections(tiles, 0, 1)), [(0,0), (0,2)])
        self.assertEqual(list(connections(tiles, 0, 2)), [(1,2), (0,1)])
        self.assertEqual(list(connections(tiles, 1, 0)), [(0,0), (2,0)])
        self.assertEqual(list(connections(tiles, 1, 1)), [])
        self.assertEqual(list(connections(tiles, 1, 2)), [(0,2), (2,2)])
        self.assertEqual(list(connections(tiles, 2, 0)), [(1,0), (2,1)])
        self.assertEqual(list(connections(tiles, 2, 1)), [(2,0), (2,2)])
        self.assertEqual(list(connections(tiles, 2, 2)), [(1,2), (2,1)])

    def test_get_path(self):
        with open(test_data['a']) as f:
            tiles = [[get_tile(c) for c in line.strip()] for line in f.readlines()]
        path = get_path(tiles)
        self.assertEqual(path, [(0,0), (1,0), (2,0), (2,1), (2,2), (1,2), (0,2), (0,1)])

    def test_get_distances(self):
        with open(test_data['a']) as f:
            tiles = [[get_tile(c) for c in line.strip()] for line in f.readlines()]
        D = get_distances(tiles)
        self.assertEqual(D.tolist(), [[0, 1, 2],[1, -1, 3],[2, 3, 4]])

    def test_get_distances(self):
        with open(test_data['b']) as f:
            tiles = [[get_tile(c) for c in line.strip()] for line in f.readlines()]
        D = get_distances(tiles)
        self.assertEqual(D.tolist(), [
            [-1,-1,-1,-1,-1],
            [-1, 0, 1, 2,-1],
            [-1, 1,-1, 3,-1],
            [-1, 2, 3, 4,-1],
            [-1,-1,-1,-1,-1]])
        
    def test_get_distances(self):
        with open(test_data['d']) as f:
            tiles = [[get_tile(c) for c in line.strip()] for line in f.readlines()]
        D = get_distances(tiles)
        self.assertEqual(D.tolist(), [
            [-1,-1, 4, 5,-1],
            [-1, 2, 3, 6,-1],
            [ 0, 1,-1, 7, 8],
            [ 1, 4, 5, 6, 7],
            [ 2, 3,-1,-1,-1]])

    def test_part_1(self):
        answ = {'a': 4, 'b': 4, 'c': 8, 'd': 8}
        for k, ans in answ.items():
            args = Namespace(file = test_data[k], part = 1, verbose = False)
            self.assertEqual(main(args), ans)

    def test_part_1_full(self):
        args = Namespace(file = full_data, part = 1, verbose = False)
        self.assertEqual(main(args), 7097)

    @unittest.skip('not implemented')
    def test_part_2(self):
        args = Namespace(file = test_data['a'], part = 2, verbose = False)
        self.assertEqual(main(args), 360)

if __name__ == '__main__':
    unittest.main()





