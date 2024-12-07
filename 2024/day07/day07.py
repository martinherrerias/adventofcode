#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
import operator
import time

OPERATORS = {'+': operator.add,
             '*': operator.mul,
             '||': lambda a, b: int(str(a) + str(b))}

# For sequences of a certain size, it should be faster too calculate upper
# and lower bounds, and check whether it's worth continuing.
# Using 2 gives the best peformance improvement for 3 operations (20-25%) 
TEST_BOUNDS_IF_LEN = 2

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('--K', type=int, default = 2,
        help='Test upper/lower bounds instead of exhaustive search for N > K')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def bounds(numbers, ops = ['+','*']):

    lower = numbers[0]
    upper = numbers[0]

    for j in range(1, len(numbers)):
        lower = min([OPERATORS[op](lower, numbers[j]) for op in ops])
        upper = max([OPERATORS[op](upper, numbers[j]) for op in ops])

    return lower, upper

def test(target, numbers, ops = ['+','*']):

    def _test(prev, op, next):
        if next == len(numbers):
            return prev == target
        
        prev = op(prev, numbers[next])

        if len(numbers) - next - 2 > TEST_BOUNDS_IF_LEN:
            lower, upper = bounds([prev] + numbers[next+1:], ops)
            if lower == target or upper == target:
                return True
            if not (lower < target < upper):
                return False

        for op in ops:
            if _test(prev, OPERATORS[op], next + 1):
                return True

        return False
    
    for op in ops:
        if _test(numbers[0], OPERATORS[op], 1):
            return target

    return 0

def part_1(target, numbers):
    return test(target, numbers, ops = ['+','*'])

def part_2(target, numbers):
    return test(target, numbers, ops = ['+','*','||'])


def parse_line(line):
    parts = line.split(': ')
    return int(parts[0]), [int(x) for x in parts[1].split()]

def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    rows = [parse_line(line) for line in lines]

    if part == 1:
        values = [part_1(*row) for row in rows]
    elif part == 2:
        values = [part_2(*row) for row in rows]
    else:
        raise ValueError(f'Invalid part number: {part}')

    total = sum(values)
    
    if verbose:
        for i, value in enumerate(values):
            print(f'{rows[i]}: {value}')

    return total


if __name__ == '__main__':

    args = parse_args()
    TEST_BOUNDS_IF_LEN = args.K

    t0 = time.time()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')

    print(f'Testing bounds for N > {TEST_BOUNDS_IF_LEN}, elapsed: {time.time() - t0}')
