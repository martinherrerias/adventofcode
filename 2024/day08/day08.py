#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
import itertools

import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    return parser.parse_args()


def antinodes(r1, c1, r2, c2, n_rows, n_cols, dist_range = None):

    dr, dc = (r2-r1), (c2 - c1)

    if dist_range is None:
        dist_range = range(max(n_rows//dr, n_cols//dc))

    nodes = [(r2 + k*dr, c2 + k*dc) for k in dist_range] + \
            [(r1 - k*dr, c1 - k*dc) for k in dist_range]
    
    return [n for n in nodes if 0 <= n[0] < n_rows and 0 <= n[1] < n_cols]


def search_antinodes(data, dist_range = [1]):

    types = [c for c in set(data.reshape(-1).tolist()) if c.isalnum()]
    
    nodes = []
    for t in types:
        r, c = np.nonzero(data == t)

        for (i,j) in itertools.combinations(range(len(r)), 2):
            nodes.extend(
                antinodes(r[i], c[i], r[j], c[j], *data.shape, dist_range)
            )

    return set(nodes)


def part_1(data):
    nodes = search_antinodes(data, dist_range=[1])
    return len(nodes)

def part_2(data):
    nodes = search_antinodes(data, dist_range=None)
    return len(nodes)

def main(file=None, part=None):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    data = np.array([list(line.strip()) for line in lines])

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
        total = main(args.file, part)
        print(f'Part {part} total: {total}')
