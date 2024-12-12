# Unit tests for src/day12.py

import os
import pytest
import numpy as np
from day12 import part_1, part_2, main, Region

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day12.test.dat')

def char_mat(*args):
    return np.array([list(x) for x in args])

def test_find_regions():
    from day12 import find_regions

    data = char_mat(
        'AAAA',
        'BBCD',
        'BBCC',
        'EEEC'
    )
    assert find_regions(data) == [Region('A', 4, 10), Region('B', 4, 8),
        Region('C', 4, 10), Region('D', 1, 4), Region('E', 3, 8)]

    data = char_mat(
        'OOOOO',
        'OXOXO',
        'OOOOO',
        'OXOXO',
        'OOOOO'
    )
    assert find_regions(data) == [Region('O', 21, 36), Region('X', 1, 4),
        Region('X', 1, 4), Region('X', 1, 4), Region('X', 1, 4)]

def test_main_1():
    assert main(file=test_data, part=1) == 1930

# def test_main_2():
#     assert main(file=test_data, part=2) == 0
