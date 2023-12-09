# Unit tests for src/template.py

import unittest
from argparse import Namespace

from template import *

import os
here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'template.test.dat')

class TestTemplate(unittest.TestCase):

    def test_parse_line(self):
        self.assertEqual(parse_line('12 3 4', 1, False), 19)
        self.assertEqual(parse_line('1 23', 2, False), 48)

    def test_part_1(self):
        args = Namespace(file = test_data, part = 1, verbose = False)
        self.assertEqual(main(args), 180)

    def test_part_2(self):
        args = Namespace(file = test_data, part = 2, verbose = False)
        self.assertEqual(main(args), 360)

if __name__ == '__main__':
    unittest.main()





