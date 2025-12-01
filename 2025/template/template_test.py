# Unit tests for src/template.py

import os
# import pytest
import numpy as np
from template import part_1, part_2, main

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "template.test.dat")


def test_part_1():
    assert part_1(np.array([1, 2, 3])) == 6


def test_part_2():
    assert part_2(np.array([1, 2, 3])) == 12


def test_main_1():
    assert main(file=test_data, part=1) == 180


def test_main_2():
    assert main(file=test_data, part=2) == 360
