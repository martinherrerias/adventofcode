# Unit tests for src/day16.py

import os
import pytest

here = os.path.dirname(os.path.realpath(__file__))


def test_main():
    from day16 import main

    test_data = os.path.join(here, 'day16.test.dat')
    assert main(file=test_data) == (7036, 45)

    test_data = os.path.join(here, 'day16.test2.dat')
    assert main(file=test_data) == (11048, 64)
