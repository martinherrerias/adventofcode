#! /usr/bin/env python3

'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import sys
import argparse
import inspect
import re
from pathlib import Path

def parse_line(line, part = 2, verbose = False):
    numbers = map(int, re.findall(r'(\d+)', line))
    return sum(numbers)*part

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

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    values = [parse_line(line, args.part, args.verbose) for line in lines]
    total = sum(values)

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

