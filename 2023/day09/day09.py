#! /usr/bin/env python3

'''
Advent of Code 2023 - Day09

'''

import sys
import argparse
import inspect
import re
import numpy as np

def parse_line(line, part = 2, verbose = False):
    numbers = np.array(list(map(int, re.findall(r'([-\d]+)', line))))
    next = predict(numbers, part, verbose)
    return next
        
def predict(numbers, part, verbose):
    d = np.diff(numbers)
    if part == 1:
        idx = -1
        sign = 1
    else:
        idx = 0
        sign = -1

    if all(d == d[0]):
        next = numbers[idx] + sign*d[0]
    else:
        next = numbers[idx] + sign*predict(d, part, verbose)
    if verbose:
        print(f'{numbers} >> {next}')
    return next

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day09.py [-v] [--part 1]
        python3 -m day09.py --file data.txt [-v] [--part 1]''')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    parser.add_argument('--file', type=str, help='Specify input file')
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

