# Unit tests for src/day03.py

import os
# import pytest

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day03.test.dat")


def test_max_joltage():
    from day03 import max_joltage
    assert max_joltage(list(map(int, list('987654321111111')))) == 98
    assert max_joltage(list(map(int, list('811111111111119')))) == 89
    assert max_joltage(list(map(int, list('234234234234278')))) == 78
    assert max_joltage(list(map(int, list('818181911112111')))) == 92


def test_main_1():
    from day03 import main
    assert main(file=test_data, part=1) == 357


def test_main_2():
    from day03 import main
    assert main(file=test_data, part=2) == 3121910778619
