# Unit tests for src/day09.py

import os
import pytest
import numpy as np
from day09 import part_1, part_2, main, GAP

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day09.test.dat')

def _as_list(row):
    return [int(x) if x.isdigit() else x for x in list(row)]

def test_unpack():
    from day09 import unpack

    assert unpack('12345') == _as_list('0..111....22222')
    assert unpack('10'*20) == list(range(20))
    assert unpack('2333133121414131402') == \
        _as_list('00...111...2...333.44.5555.6666.777.888899')

def test_compact():
    from day09 import compact

    assert compact(_as_list('......1.2..34')) == _as_list("4321")
    assert compact(_as_list('123.4.')) == _as_list("1234")

    assert compact(_as_list('00...111...2...333.44.5555.6666.777.888899')) == \
        _as_list("0099811188827773336446555566")

def test_checksum():
    from day09 import checksum
    assert checksum(_as_list('0099811188827773336446555566')) == 1928

# def test_part_2():
#     assert part_2(np.array([1, 2, 3])) == 12

def test_main_1():
    assert main(file=test_data, part=1) == 1928

# def test_main_2():
#     assert main(file=test_data, part=2) == 360

# 6154342787400