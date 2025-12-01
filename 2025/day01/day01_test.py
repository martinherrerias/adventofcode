# Unit tests for src/day01.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day01.test.dat")


def test_turn():
    from day01 import Turn
    t = Turn('R42')
    assert t.direction == 1 and t.clicks == 42
    assert t.apply(1) == 43
    assert t.apply(99) == 41

    t = Turn('L10')
    assert t.direction == -1 and t.clicks == 10
    assert t.apply(5) == 95

    assert Turn('R5').apply(95) == 0


# def test_part_1():
#     assert part_1(np.array([1, 2, 3])) == 6


# def test_part_2():
#     assert part_2(np.array([1, 2, 3])) == 12


def test_main_1():
    from day01 import main
    assert main(file=test_data, part=1) == 3


# def test_main_2():
#     assert main(file=test_data, part=2) == 360
