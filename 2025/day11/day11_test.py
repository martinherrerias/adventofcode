# Unit tests for src/day11.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data_1 = os.path.join(here, "day11_test_1.dat")
test_data_2 = os.path.join(here, "day11_test_2.dat")


def test_main_1():
    from day11 import main
    assert main(file=test_data_1, part=1) == 5


def test_main_2():
    from day11 import main
    assert main(file=test_data_2, part=2) == 2
