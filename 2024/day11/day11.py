#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from math import log10
from itertools import chain

import numpy as np

N_BLINKS = 25

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def digits(n):
    return int(log10(n))+1

def shift_stone(n):
    if n == 0:
        return [1]
    elif digits(n) % 2 == 0:
        n_str = str(n)
        return [int(n_str[:len(n_str)//2]), int(n_str[len(n_str)//2:])]
    else:
        return [n*2024]

def blink(stones):
    new_stones = [shift_stone(stone) for stone in stones]
    return list(chain(*new_stones))

def part_1(data):
    for _ in range(N_BLINKS):
        data = blink(data)
    return len(data)

def part_2(row):
    return 0


def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    # Numeric row-wise
    data = [int(x) for x in lines[0].split()]

    if part == 1:
        total = part_1(data)
    elif part == 2:
        total = part_2(data)
    else:
        raise ValueError(f'Invalid part number: {part}')

    return total


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
