# Unit tests for src/day08.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day08.test.dat")


def test_main_1():
    from day08 import main
    assert main(file=test_data, part=1, n=10) == 40


def test_main_2():
    from day08 import main
    assert main(file=test_data, part=2) == 25272
