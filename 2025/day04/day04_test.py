# Unit tests for src/day04.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day04.test.dat")


def test_main_1():
    from day04 import main
    assert main(file=test_data, part=1) == 13
