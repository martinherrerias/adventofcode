# Unit tests for src/day07.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day07.test.dat")


def test_main_1():
    from day07 import main
    assert main(file=test_data, part=1) == 21


def test_main_2():
    from day07 import main
    assert main(file=test_data, part=2) == 40
