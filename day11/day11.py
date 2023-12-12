#! /usr/bin/env python3

'''
Advent of Code 2023 - Day11
'''

import sys
import argparse
import inspect
import numpy as np
import itertools

def expand(x, scale = 2):
    x = np.array(x, dtype=bool)
    scale = int(scale)
    xx = np.cumsum(~x*(scale-1) + int(1)) - (~x[0]*(scale-1)) - 1
    return xx

def dist(xi, yi, xj, yj):
    return abs(xi - xj) + abs(yi - yj)

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day11.py [-v] [--part 1]
        python3 -m day11.py --file data.txt [-v] [--part 1]''')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--scale', type=int, default=2, help='Specify the expansion scale')
    parser.add_argument('--file', type=str, help='Specify input file')
    return parser.parse_args()

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    stars = np.array([list(line.strip()) for line in lines]) == '#'

    x = expand(np.any(stars, axis=0), args.scale)
    y = expand(np.any(stars, axis=1), args.scale)
    r, c = np.where(stars)
    coords = list(zip(x[c], y[r]))

    total = 0
    for i, j in itertools.combinations(range(len(coords)), 2):
        
        d = dist(*coords[i], *coords[j])
        total += d
        if args.verbose:
            print(f'{i+1}:({coords[i]}) -> {j+1}:({coords[j]}) = {d}')

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

