# Unit tests for src/day02.py

import os

here = os.path.dirname(os.path.realpath(__file__))
test_data = os.path.join(here, "day02.test.dat")


def test_part_1():
    from day02 import find_twin_numbers

    assert find_twin_numbers('11-22') == {11, 22}
    assert find_twin_numbers('95-115') == {99}
    assert find_twin_numbers('998-1012') == {1010}
    assert find_twin_numbers('1188511880-1188511890') == {1188511885}
    assert find_twin_numbers('222220-222224') == {222222}
    assert find_twin_numbers('1698522-1698528') == set()
    assert find_twin_numbers('446443-446449') == {446446}
    assert find_twin_numbers('38593856-38593862') == {38593859}

    assert find_twin_numbers('1-1') == set()
    assert find_twin_numbers('10-99') == {11*i for i in range(1, 10)}
    assert find_twin_numbers('100-1009') == set()


def test_part_2():
    from day02 import find_rep_numbers

    assert find_rep_numbers('11-22') == {11, 22}
    assert find_rep_numbers('95-115') == {99, 111}
    assert find_rep_numbers('998-1012') == {999, 1010}
    assert find_rep_numbers('1188511880-1188511890') == {1188511885}
    assert find_rep_numbers('222220-222224') == {222222}
    assert find_rep_numbers('1698522-1698528') == set()
    assert find_rep_numbers('446443-446449') == {446446}
    assert find_rep_numbers('38593856-38593862') == {38593859}
    assert find_rep_numbers('565653-565659') == {565656}
    assert find_rep_numbers('824824821-824824827') == {824824824}
    assert find_rep_numbers('2121212118-2121212124') == {2121212121}

    assert find_rep_numbers('1-1') == set()
    assert find_rep_numbers('1-99') == {11*i for i in range(1, 10)}
    assert find_rep_numbers('100-999') == {111*i for i in range(1, 10)}


def test_main_1():
    from day02 import main
    assert main(file=test_data, part=1) == 1227775554


def test_main_2():
    from day02 import main
    assert main(file=test_data, part=2) == 4174379265
