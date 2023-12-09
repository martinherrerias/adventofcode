#! /usr/bin/env python3

'''
Advent of Code 2023 - Day06

'''

import sys
import argparse
import inspect
import re
from math import sqrt, floor, ceil, prod

def race(time, dist, verbose = False):
    
    # t = np.array(range(time))
    # d = t*(time - t)
    # values = t[d > dist]
    # n = len(values)

    k = sqrt(max(0,time**2/4 - dist))
    values = range(floor(time/2 - k + 1), ceil(time/2 + k - 1) + 1)
    n = len(values)

    if verbose:
            print(f'Time: {time}, Dist: {dist} >> n = {n}, values = {values}')

    return n

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day06.py [-v] [--part 1]
        python3 -m day06.py --file data.txt [-v] [--part 1]''')
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

    time = re.findall(r'\d+', lines[0])
    dist = re.findall(r'\d+', lines[1])

    if args.part == 1:
        time = list(map(int, time))
        dist = list(map(int, dist))

        values = map(race, time, dist, [args.verbose]*len(time))
        result = prod(values)
    else:
        time = int(''.join(time))
        dist = int(''.join(dist))
        result = race(time, dist, args.verbose)
    
    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return result
    else:
        print(f'Score: {result}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

