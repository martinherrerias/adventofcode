#! /usr/bin/env python3

'''
Advent of Code 2024 - https://adventofcode.com/2024/day/2
'''

import sys
import argparse
import inspect
import numpy as np
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        usage=f'python3 {Path(__file__).name} [--file DATA] [--part N] [-v]')
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat').name, 
        help='Specify input file, default: %(default)s')
    parser.add_argument('--part', type=int, default=1, help='Part number, default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    return parser.parse_args()

def parse_line(line, part = 2, verbose = False):
    numbers = np.fromstring(line, dtype=int, sep=' ')

    return sum(numbers)*part

def safe(row):
    """
    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.
    """
    d = np.diff(row)
    ok = np.all((d >= 1) & (d <= 3)) | \
         np.all((d <= -1) & (d >= -3))
    return ok

def almost_safe(row):
    """
    Tolerate a single bad level in what would otherwise be a safe report
    """
    if safe(row):
        return True
    for i in range(len(row)):
        if safe(np.delete(row, i)):
            return True
    return False

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    rows = [np.fromstring(line, dtype=int, sep=' ') for line in lines]

    if args.part == 1:
        values = [safe(row) for row in rows]
    elif args.part == 2:
        values = [almost_safe(row) for row in rows]
    else:
        raise ValueError(f'Invalid part number: {args.part}')
    
    if args.verbose:
        for i, value in enumerate(values):
            print(f'{rows[i]}: {value}')

    total = sum(values)

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

