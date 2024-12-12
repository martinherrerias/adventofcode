# Unit tests for src/day11.py

import os
import pytest
from numpy import nan
from math import isnan

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day11.test.dat')

def test_shift_stone():
    from day11 import shift_stone

    assert shift_stone(0) == [1]
    assert shift_stone(1) == [2024]
    assert shift_stone(10) == [1,0]
    assert shift_stone(99) == [9,9]
    assert shift_stone(999) == [2021976]

def test_blinks_graph():
    from day11 import blinks_graph

    assert blinks_graph([0,1,10], 1) == {0: [1], 1: [2024], 10: [1,0]}
    assert blinks_graph([0,1,10], 2) == {0: [1], 1: [2024], 10: [1,0], 2024: [20,24]}

def test_cleanup_graph():
    from day11 import cleanup_graph

    graph, node_map = cleanup_graph({0: [1], 1: [2024], 10: [1,0], 2024: [20,24]})
    assert graph == {0: [1], 1: [3], 2: [1,0], 3: [4,4], 4: []}
    assert node_map == {0: 0, 1: 1, 10: 2, 2024: 3, 20: 4, 24: 4}

def test_count_paths():
    from day11 import count_paths

    graph = {0: [1], 1: [3], 2: [1,0], 3: [4,4], 4: []}

    counts = count_paths(graph, 1) # == {0: 1, 1: 1, 2: 2, 3: 2, 4: nan}
    assert [counts[j] for j in range(4)] == [1, 1, 2, 2]
    assert isnan(counts[4])

    counts = count_paths(graph, 2) # == {0: 1, 1: 2, 2: 2, 3: nan, 4: nan}
    assert [counts[j] for j in range(3)] == [1, 2, 2]
    assert all(isnan(counts[j]) for j in [3,4])

def test_many_blinks():
    from day11 import many_blinks

    assert many_blinks([125, 17], 25) == 55312

def test_main_1():
    from day11 import main
    assert main(file=test_data, part=1) == 55312
