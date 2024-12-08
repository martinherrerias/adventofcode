# Unit tests for src/day08.py

import os
import pytest
from day08 import main

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day08.test.dat')

def test_main_1():
    assert main(file=test_data, part=1) == 14

def test_main_2():
    assert main(file=test_data, part=2) == 34
