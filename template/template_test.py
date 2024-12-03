# Unit tests for src/template.py

import os
import unittest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'template.test.dat')

class TestTemplate(unittest.TestCase):

    def test_part_1(self):
        from template import part_1
        self.assertEqual(part_1(np.array([1, 2, 3])), 6)

    def test_part_2(self):
        from template import part_2
        self.assertEqual(part_2(np.array([1, 2, 3])), 12)

    def test_main_1(self):
        from template import main
        self.assertEqual(main(file = test_data, part = 1), 180)

    def test_main_2(self):
        from template import main
        self.assertEqual(main(file = test_data, part = 2), 360)

if __name__ == '__main__':
    unittest.main()
