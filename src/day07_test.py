# Unit tests for src/day07.py

import unittest
from argparse import Namespace

from day07 import *

class TestDay07(unittest.TestCase):

    def test_parse_input(self):

        hand, bid, idx, counts = parse_input('AKQJT 123', 1)
        self.assertEqual(hand, 'AKQJT')
        self.assertEqual(bid, 123)
        self.assertEqual(idx, (13,12,11,10,9))
        self.assertEqual(counts, (1,1,1,1,1))

        hand, bid, idx, counts = parse_input('22233 1', 1)
        self.assertEqual(hand, '22233')
        self.assertEqual(idx, (1,1,1,2,2))
        self.assertEqual(counts, (3,2,0,0,0))

        hand, bid, idx, counts = parse_input('42TT2 1', 1)
        self.assertEqual(hand, '42TT2')
        self.assertEqual(counts, (2,2,1,0,0))

    def test_rank(self):
        r = sort_index([(2,1,0),(3,0,0),(1,1,1)], [(0,0),(0,0),(0,0)])
        self.assertEqual(list(r), [2,0,1])

        r = sort_index([(2,1,0),(3,0,0),(1,1,1)], [(2,1),(3,0),(2,2)])
        self.assertEqual(list(r), [2,0,1])

        r = sort_index([(1,1,1),(1,1,1),(1,1,1)], [(2,1),(3,0),(2,2)])
        self.assertEqual(list(r), [0,2,1])

    def test_part_1(self):
        args = Namespace(file = 'test_data/day07.txt', part = 1, verbose = False)
        self.assertEqual(main(args), 6440)

    def test_part_2(self):
        args = Namespace(file = 'test_data/day07.txt', part = 2, verbose = False)
        self.assertEqual(main(args), 5905)

        args = Namespace(file = 'data/day07.txt', part = 2, verbose = False)
        self.assertEqual(main(args), 251515496)

if __name__ == '__main__':
    unittest.main()





