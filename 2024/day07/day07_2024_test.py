# Unit tests for src/day07.py

import os
import pytest
from day07 import part_1, part_2, main, parse_line

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day07.test.dat')

def test_parse_line():
    assert parse_line('1: 2 3 4') == (1, [2,3,4])

def test_part_1():
    for r in range(40):
        if r in [10,24,13,36,9,20]:
            assert part_1(r, [1, 2, 3, 4]) == r
        else:
            assert part_1(r, [1, 2, 3, 4]) == 0

def test_part_2():
    for r in range(30):
        if r in [5,6,23]:
            assert part_2(r, [2,3]) == r

def test_main_1():
    assert main(file=test_data, part=1) == 3749

def test_main_2():
    assert main(file=test_data, part=2) == 11387
