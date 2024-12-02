#! /usr/bin/env python3

'''
Advent of Code 2023 - Day01

'''

import sys
import argparse
import inspect

def do_stuff(line, part = 2, verbose = False):
    value = part
    if verbose:
        print(f'{line} >> {value}')
    return value

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day01.py [-v] [--part 1]
        python3 -m day01.py --file data.txt [-v] [--part 1]''')
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

    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue

        value = do_stuff(line, args.part, args.verbose)
        total += value

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

