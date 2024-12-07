#! /usr/bin/env python3

'''
Advent of Code 2024 - https://adventofcode.com/2024/day/1
'''

import sys
import argparse
import inspect
import re
import numpy as np
from pathlib import Path

def parse_line(line, part = 2, verbose = False):
    numbers = map(int, re.findall(r'(\d+)', line))
    return sum(numbers)*part

def parse_args():
    parser = argparse.ArgumentParser(
        usage=f'python3 {Path(__file__).name} [--file DATA] [--part N] [-v]')
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat').name, 
        help='Specify input file, default: %(default)s')
    parser.add_argument('--part', type=int, default=1, help='Part number, default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    return parser.parse_args()

def part1(data):
    return sum(abs(np.sort(data[:,1]) - np.sort(data[:,0])))

def part2(data):
    total = 0
    for i in set(data[:,0]):
        total += i * sum(data[:,0] == i) * sum(data[:,1] == i)
    return total

def main(args):

    # read delimited file (two columns)
    if args.file:
        with open(args.file) as f:
            data = np.genfromtxt(f)

    if args.part == 1:
        total = part1(data)
    elif args.part == 2:
        total = part2(data)
    else:
        raise ValueError(f'Invalid part number: {args.part}')

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

