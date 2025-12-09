# Unit tests for src/day09.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day09.test.dat")


def test_main_1():
    from day09 import main
    assert main(file=test_data, part=1) == 50


def test_main_2():
    from day09 import main
    assert main(file=test_data, part=2) == 24
