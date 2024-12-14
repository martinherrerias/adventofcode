# Unit tests for src/day14.py

import os
import pytest
import numpy as np

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day14.test.dat')

def test_main_1():
    from day14 import main
    assert main(file=test_data, part=1) == 12

