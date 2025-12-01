# Unit tests for src/day01.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day01.test.dat")


def test_turn():
    from day01 import Turn
    t = Turn('R42')
    assert t.direction == 1 and t.clicks == 42
    assert t.apply(1) == (43, 0)
    assert t.apply(99) == (41, 1)

    t = Turn('L10')
    assert t.direction == -1 and t.clicks == 10
    assert t.apply(5) == (95, 1)

    assert Turn('R5').apply(95) == (0, 1)

    assert Turn('R0').apply(0) == (0, 0)
    assert Turn('L0').apply(0) == (0, 0)
    assert Turn('R5').apply(0) == (5, 0)
    assert Turn('L5').apply(0) == (95, 0)
    assert Turn('R100').apply(0) == (0, 1)
    assert Turn('L100').apply(0) == (0, 1)

    assert Turn('R105').apply(95) == (0, 2)
    assert Turn('L110').apply(5) == (95, 2)
    assert Turn('R1000').apply(50) == (50, 10)


def test_main_1():
    from day01 import main
    assert main(file=test_data, part=1) == 3


def test_main_2():
    from day01 import main
    assert main(file=test_data, part=2) == 6
