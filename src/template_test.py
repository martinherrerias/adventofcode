# Unit tests for src/template.py

import unittest
from argparse import Namespace

from template import *

class TestTemplate(unittest.TestCase):

    def test_do_stuff(self):
        self.assertEqual(do_stuff('foo', 1, False), 1)

    def test_part_1(self):
        args = Namespace(file = 'test_data/template.txt', part = 1, verbose = False)
        best = main(args)
        self.assertEqual(best, 1)

    def test_part_2(self):
        args = Namespace(file = 'test_data/template.txt', part = 2, verbose = False)
        best = main(args)
        self.assertEqual(best, 2)

if __name__ == '__main__':
    unittest.main()





