# Unit tests for src/day13.py

import os
import pytest
import numpy as np
from textwrap import dedent

from day13 import part_1, part_2, main, Problem

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day13.test.dat')

def test_parse_input():
    from day13 import parse_input
    
    text = dedent("""\
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
    """)
    assert parse_input(text) == Problem((94, 34), (22, 67), (8400, 5400))

def test_part_1():
    assert part_1(Problem((94, 34), (22, 67), (8400, 5400))) == 280
    assert part_1(Problem((26, 66), (67, 21), (12748, 12176))) == None
    assert part_1(Problem((17, 86), (84, 37), (7870, 6450))) == 200
    assert part_1(Problem((69, 23), (27, 71), (18641, 10279))) == None

def test_part_2():
    assert part_2(Problem((94, 34), (22, 67), (8400, 5400))) == None
    assert part_2(Problem((26, 66), (67, 21), (12748, 12176))) > 0
    assert part_2(Problem((17, 86), (84, 37), (7870, 6450))) == None
    assert part_2(Problem((69, 23), (27, 71), (18641, 10279))) > 0

def test_main_1():
    assert main(file=test_data, part=1) == 480
