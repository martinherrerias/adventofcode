# Unit tests for src/day06.py

import os
import pytest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day06.test.dat')

@pytest.mark.parametrize("input,output,reverse,idx", 
                         [('^..#.', 'XXX#.', False, 2),
                          ('^...', 'XXXX', False, 4),
                          ('^#..', 'X#..', False, 0),
                          ('.#..^', '.#XXX', True, 2),
                          ('...^', 'XXXX', True, 4),
                          ('..#^', '..#X', True, 0),
                          ('#.^', '#XX', True, 1)])
def test_move(input,output,reverse,idx):

    from day06 import move

    out, out_idx = move(np.array(list(input)), reverse=reverse)
    assert ''.join(out) == output
    assert out_idx == idx

def test_part_1():

    from day06 import trace_path, part_1

    grid = lambda x: np.array([list(l) for l in x])
    input = ['.#...',
             '....#',
             '.^...']
    output = ['.#...',
              '.XXX#',
              '.^.X.']
    walked, _ = trace_path(grid(input))
    assert np.array_equal(grid(walked), grid(output))

# def test_part_2():
#     assert part_2(np.array([1, 2, 3])) == 12

def test_main_1():
    from day06 import main
    assert main(file=test_data, part=1) == 41

def test_main_2():
    from day06 import main
    assert main(file=test_data, part=2) == 6
