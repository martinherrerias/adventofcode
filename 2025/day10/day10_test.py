# Unit tests for src/day10.py

import os

# import pytest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day10.test.dat")


def test_parse_line():
    from day10 import parse_line

    m, s, j = parse_line("[.#.] (0) (1,2) {1,2,3}")
    assert np.array_equal(m, [[1, 0], [0, 1], [0, 1]])
    assert np.array_equal(s, [0, 1, 0])
    assert np.array_equal(j, [1, 2, 3])


def test_part_1():
    from day10 import part_1

    assert part_1("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}") == 2
    assert part_1("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}") == 3
    assert part_1("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}") == 2


def test_part_2():
    from day10 import part_2

    assert part_2("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}") == 10
    assert part_2("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}") == 12
    assert part_2("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}") == 11


def test_main_1():
    from day10 import main
    assert main(file=test_data, part=1) == 7


def test_main_2():
    from day10 import main
    assert main(file=test_data, part=2) == 33
