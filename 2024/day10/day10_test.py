# Unit tests for src/day10.py

import os
import pytest
import numpy as np
from day10 import part_1, part_2, main

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day10.test.dat')

def test_follow_trail():
    from day10 import follow_trail
    data = np.array([[0,1,2],[5,4,3],[6,7,8],[1,0,9]])
    assert follow_trail(data,0,0) == 1

def test_main_1():
    assert main(file=test_data, part=1) == 36

def test_main_2():
    assert main(file=test_data, part=2) == 81
