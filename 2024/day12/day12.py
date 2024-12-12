#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path

import numpy as np
from collections import namedtuple

PADDING = '.'

Region = namedtuple('Region', ['tag', 'area', 'perimeter'])

def next_seed(used):
    for index, isused in np.ndenumerate(used):
        if ~isused:
            return index
    return None

def find_regions(data):

    used = np.zeros(data.shape, bool)
    data = np.pad(data, 1, constant_values=PADDING)
    used = np.pad(used, 1, constant_values=True)

    r_offset = np.array([1, -1, 0, 0])
    c_offset = np.array([0, 0, -1, 1])

    def grow(r0, c0, a = 0, p = 0):

        nonlocal used

        used[r0, c0] = True
        a += 1

        next_r = r0 + r_offset
        next_c = c0 + c_offset
        
        foreign = data[next_r, next_c] != data[r0, c0]
        p += sum(foreign)

        heads = ~used[next_r, next_c] & ~foreign
        hr, hc = next_r[heads], next_c[heads]
        used[hr, hc] = True

        for r, c in zip(hr, hc):
            a, p = grow(r, c, a, p)

        return a, p
    
    regions = []
    seed = (1,1)
    while seed:
        r0, c0 = seed
        a, p = grow(r0, c0)
        regions.append(Region(data[r0, c0], a, p))
        seed = next_seed(used)

    return sorted(regions, key=lambda r: r.tag)


def part_1(data):
    regions = find_regions(data)
    return sum(r.area*r.perimeter for r in regions)

def part_2(data):
    return 0

def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    data = np.array([list(line.strip()) for line in lines])

    if part == 1:
        total = part_1(data)
    elif part == 2:
        total = part_2(data)
    else:
        raise ValueError(f'Invalid part number: {part}')
    
    if verbose:
        for i, value in enumerate(values):
            print(f'{rows[i]}: {value}')

    return total


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
