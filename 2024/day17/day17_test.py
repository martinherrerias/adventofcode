# Unit tests for src/day17.py

import os
import pytest

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day17.test.dat')

def test_individual():
    from day17 import Computer

    cmp = Computer(0, 0, 9, [2, 6])
    cmp.run()
    assert cmp.reg_b == 1

    cmp = Computer(10, 0, 0, [5, 0, 5, 1, 5, 4])
    cmp.run()
    assert cmp.out == [0, 1, 2]

    cmp = Computer(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    cmp.run()
    assert cmp.out == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert cmp.reg_a == 0

    cmp = Computer(0, 29, 0, [1, 7])
    cmp.run()
    assert cmp.reg_b == 26

    cmp = Computer(0, 2024, 43690, [4, 0])
    cmp.run()
    assert cmp.reg_b == 44354

    # not in docs, for full coverage
    cmp = Computer(125, 3, 2, [6, 5, 7, 6])
    cmp.run()
    assert cmp.reg_a == 125
    assert cmp.reg_b == 15
    assert cmp.reg_c == 31


def test_part_1():
    from day17 import Computer
    cmp = Computer.from_file(test_data)
    cmp.run()
    assert cmp.out == [4,6,3,5,6,3,5,2,1,0]

# def test_part_2():
#     assert part_2(np.array([1, 2, 3])) == 12

def test_main_1():
    from day17 import main
    assert main(file=test_data, part=1) == '4,6,3,5,6,3,5,2,1,0'

# def test_main_2():
#     assert main(file=test_data, part=2) == 360
