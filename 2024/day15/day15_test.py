# Unit tests for src/day15.py

import os
import pytest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day15.test.dat')
mini_test = os.path.join(here, 'day15.mini.dat')

def test_move_in_row():
    """
    @O..# -> .@O.#, if reverse: 
    """
    from day15 import move_in_row

    row = np.array(list('@O..#'))
    moved = move_in_row(row)
    assert ''.join(row) == '.@O.#' and moved

    row = np.array(list('#..O@'))
    moved = move_in_row(row, reverse=True)
    assert ''.join(row) == '#.O@.' and moved

    row = np.array(list('@OO#'))
    moved = move_in_row(row)
    assert ''.join(row) == '@OO#' and not moved

    row = np.array(list('@O#.#'))
    moved = move_in_row(row)
    assert ''.join(row) == '@O#.#' and not moved

    row = np.array(list('#.#O@'))
    moved = move_in_row(row, reverse=True)
    assert ''.join(row) == '#.#O@' and not moved

def test_main_1():
    from day15 import main
    assert main(file=mini_test, part=1) == 2028
    assert main(file=test_data, part=1) == 10092

def test_main_2():
    assert main(file=test_data, part=2) == 360
