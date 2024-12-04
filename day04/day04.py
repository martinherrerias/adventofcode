#! /usr/bin/env python3

'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import sys
import argparse
from pathlib import Path

import numpy as np

PADDING = '.'

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

def part_1(data: np.array):

    WORD = 'XMAS'

    data = np.pad(data, len(WORD), constant_values=PADDING)

    ncols = data.shape[1]
    data = data.reshape(-1)

    directions = np.array([1, -1, ncols, -ncols, 1+ncols, 1-ncols, -1+ncols, -1-ncols])
    starts = np.where(data == WORD[0])[0].reshape(-1, 1)

    valid = np.ones((len(starts), len(directions)), dtype=bool)
    for j, w in enumerate(WORD[1:]):
        next = starts + directions * (j+1)
        valid[valid] = data[next[valid]] == w

    return np.sum(valid)

def part_2(data):

    WORD = 'MAS'

    data = np.pad(data, 1, constant_values=PADDING)

    ncols = data.shape[1]
    data = data.reshape(-1)

    directions = np.array([1+ncols, 1-ncols, -1+ncols, -1-ncols])
    starts = np.where(data == WORD[1])[0].reshape(-1, 1)

    next = starts + directions
    prev = starts - directions
    valid = np.sum((data[next] == WORD[0]) & (data[prev] == WORD[2]), axis=1) == 2

    return np.sum(valid)

def main(file=None, part=None, verbose=False):

    if file:
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    data = np.array([list(line.strip()) for line in lines])

    if part == 1:
        total = part_1(data)
    elif part == 2:
        total = part_2(data)
    else:
        raise ValueError(f'Invalid part number: {part}')

    # if verbose:
    #     for i, value in enumerate(values):
    #         print(f'{rows[i]}: {value}')

    return total

if __name__ == '__main__':
    args = parse_args()
    total = main(**vars(args))
    print(f'Score: {total}')
