#! /usr/bin/env python3

'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import sys
import argparse
import inspect
from pathlib import Path

import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(
        usage=f'python3 {Path(__file__).name} [--file DATA] [--part N] [-v]'
              f'cat DATA | {Path(__file__).name} [--part 1] [-v]'
    )
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat').name, 
        help='Specify input file, default: %(default)s')
    parser.add_argument('--part', type=int, default=1, help='Part number, default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    return parser.parse_args()

def part_1(row):
    return sum(row)

def part_2(row):
    return sum(row) * 2

def main(file=None, part=None, verbose=False):

    if file:
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    rows = [np.fromstring(line, dtype=int, sep=' ') for line in lines]

    if part == 1:
        values = [part_1(row) for row in rows]
    elif part == 2:
        values = [part_2(row) for row in rows]
    else:
        raise ValueError(f'Invalid part number: {part}')

    total = sum(values)

    if verbose:
        for i, value in enumerate(values):
            print(f'{rows[i]}: {value}')

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(**vars(args))
