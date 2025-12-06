# Unit tests for src/day06.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day06.test.dat")


def test_main_1():
    from day06 import main
    assert main(file=test_data, part=1) == 4277556


def test_main_2():
    from day06 import main
    assert main(file=test_data, part=2) == 3263827
