#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from itertools import chain

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def follow_trail(data,r0,c0):

    nr, nc = data.shape[0], data.shape[1]

    r_offset = np.array([1, -1, 0, 0])
    c_offset = np.array([0, 0, 1, -1])

    trailheads = []
    rating = 0

    def follow_branch(r, c):

        nonlocal trailheads
        nonlocal rating

        if data[r,c] == 9:
            trailheads.append((r,c))
            rating += 1
            return []

        next_r = r + r_offset
        next_c = c + c_offset
        valid = (0 <= next_r) & (next_r < nr) & (0 <= next_c) & (next_c < nc)
        valid[valid] = data[next_r[valid], next_c[valid]] - data[r,c] == 1
            
        if not any(valid):
            return []
        
        return list(zip(next_r[valid], next_c[valid]))

    next_moves = [(r0, c0)]
    while next_moves:
        assert isinstance(next_moves[0], tuple)
        next_moves = list(chain.from_iterable(
            follow_branch(*rc) for rc in next_moves
        ))

    return len(set(trailheads)), rating


def find_trails(data, verbose=False):
    r0, c0 = np.nonzero(data == 0)
    heads, rating = zip(*[follow_trail(data, *rc) for rc in zip(r0, c0)])
    return sum(heads), sum(rating)

def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    data = np.array([[int(c) for c in list(line.strip())] for line in lines])

    heads, rating = find_trails(data, verbose)

    if part == 1:
        return heads
    elif part == 2:
        return rating
    else:
        raise ValueError(f'Invalid part number: {part}')


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
