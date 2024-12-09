#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path

import numpy as np

GAP = '.'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def unpack(row):

    row = [int(c) for c in list(row)]

    chunks = [None] * len(row)
    chunks[0::2] = [[i]*n for i, n in enumerate(row[0::2])]
    chunks[1::2] = [[GAP]*n for n in row[1::2]]

    return [i for c in chunks for i in c]

def compact(unpacked):

    assert isinstance(unpacked, list)

    gap_idx = [i for i,c in enumerate(unpacked) if not isinstance(c, int)]
    num_idx = [i for i,c in enumerate(unpacked) if isinstance(c, int)]
    num_idx.reverse()

    last_replaced = 0
    for i, g in enumerate(gap_idx):

        if i >= len(num_idx):
            return compact(unpacked) # start over

        # stop when gap is after replacing number
        if g > num_idx[i]:
            last = max(num_idx[i], last_replaced)

            # assert all(x == GAP for x in unpacked[last+1:])
            # assert all(isinstance(x, int) for x in unpacked[:last+1])

            return unpacked[:last+1]

        unpacked[g] = unpacked[num_idx[i]]
        unpacked[num_idx[i]] = GAP
        last_replaced = g

    return unpacked[:last_replaced+1]

def checksum(compacted):

    assert isinstance(compacted, list) and all([isinstance(x, int) for x in compacted])

    total = 0
    for i, n in enumerate(compacted):
        total += i*n
    return total

def part_1(row):
    return checksum(compact(unpack(row)))

def part_2(row):
    return 0


def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 1
    data = lines[0].strip()

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
