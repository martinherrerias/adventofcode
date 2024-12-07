# Unit tests for src/day03.py

import os
import pytest

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, 'day03.dat')


def test_part_1():
    from day03 import part_1
    assert part_1('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))') == 161

def test_part_2():
    from day03 import part_2
    assert part_2('mul(1,3)') == 3
    assert part_2("do()mul(1,3)don't()") == 3
    assert part_2("do()mul(1,3)don't()mul(2,4)") == 3
    assert part_2("don't()mul(1,3)do()mul(2,4)t") == 8
    assert part_2("mul(1,1)do()mul(1,1)do()mul(1,1)") == 3
    assert part_2("don't()mul(1,1)do()mul(1,1)don't()mul(1,1)") == 1
    assert part_2("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))") == 48

def test_main_1():
    from day03 import main
    assert main(file = test_data, part = 1) == 170807108

def test_main_2():
    from day03 import main
    assert main(file = test_data, part = 2) == 74838033

if __name__ == '__main__':
    pytest.main()
