# Unit tests for src/DAYN.py

import os
# import pytest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "DAYN.test.dat")


def test_part_1():
    from DAYN import part_1
    assert part_1(np.array([1, 2, 3])) == 6


def test_part_2():
    from DAYN import part_2
    assert part_2(np.array([1, 2, 3])) == 12


def test_main_1():
    from DAYN import main
    assert main(file=test_data, part=1) == 180


def test_main_2():
    from DAYN import main
    assert main(file=test_data, part=2) == 360
