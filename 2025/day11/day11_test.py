# Unit tests for src/day11.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day11.test.dat")


def test_main_1():
    from day11 import main
    assert main(file=test_data, part=1) == 5
