# Unit tests for src/day04.py

import os
import unittest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day04.test.dat')

def char_mat(*args):
    return np.array([list(x) for x in args])

class TestDay04(unittest.TestCase):

    def test_part_1(self):
        from day04 import part_1
        self.assertEqual(
            part_1(char_mat(
                'X...S',
                'MM..A',
                'A.A.M',
                'S..SX')), 3
        )

    def test_part_2(self):
        from day04 import part_2
        self.assertEqual(part_2(char_mat('M.S','.A.','M.S')), 1)
        self.assertEqual(part_2(char_mat('S.S','.A.','M.M')), 1)

    def test_main_1(self):
        from day04 import main
        self.assertEqual(main(file = test_data, part = 1), 18)

    def test_main_2(self):
        from day04 import main
        self.assertEqual(main(file = test_data, part = 2), 9)

if __name__ == '__main__':
    unittest.main()
