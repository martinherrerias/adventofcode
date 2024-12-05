# Unit tests for src/day05.py

import os
import pytest
import numpy as np
from day05 import part_1, part_2, main

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day05.test.dat')

def test_part_1():
    assert part_1([[1,2],[2,3]], np.array([1,2,3])) == 2
    assert part_1([[2,3],[1,2]], np.array([1,2,3])) == 0

def test_part_2():
    assert part_2(np.array([1, 2, 3])) == 12

def test_main_1():
    assert main(file=test_data, part=1) == 143

def test_main_2():
    assert main(file=test_data, part=2) == 360
