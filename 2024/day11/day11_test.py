# Unit tests for src/day11.py

import os
import pytest
import numpy as np
from day11 import part_1, part_2, main

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day11.test.dat')

def test_shift_stone():
    from day11 import shift_stone

    assert shift_stone(0) == [1]
    assert shift_stone(1) == [2024]
    assert shift_stone(10) == [1,0]
    assert shift_stone(99) == [9,9]
    assert shift_stone(999) == [2021976]

def test_blink():
    from day11 import blink
    assert blink([0, 1, 10, 99, 999]) == [1, 2024, 1, 0, 9, 9, 2021976]

    x = [125, 17]
    for _ in range(6):
        x = blink(x)
    assert x == [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]

def test_main_1():
    assert main(file=test_data, part=1) == 55312

def test_main_2():
    assert main(file=test_data, part=2) == 360
