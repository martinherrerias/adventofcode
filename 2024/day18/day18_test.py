# Unit tests for src/day18.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day18.test.dat')

def test_part_1():
    from day18 import Maze2
    maze = Maze2(test_data, size=(7,7))
    assert maze.solve(t = 12) == 22
    assert maze.first_unsolvable() == (6, 1)
