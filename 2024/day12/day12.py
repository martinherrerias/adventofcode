#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path

import numpy as np
from collections import namedtuple

PADDING = '.'

Region = namedtuple('Region', ['tag', 'area', 'perimeter', 'sides'])

def next_seed(used):
    for index, isused in np.ndenumerate(used):
        if ~isused:
            return index
    return None

def find_regions(data):

    r_offset = np.array([1, -1, 0, 0])
    c_offset = np.array([0, 0, -1, 1])
    DOWN, UP, LEFT, RIGHT = 0, 1, 2, 3

    used = np.zeros(data.shape, bool)

    data = np.pad(data, 1, constant_values=PADDING)
    used = np.pad(used, 1, constant_values=True)

    edges = np.zeros(data.shape + (4,), bool) # one for each direction

    def grow(r0, c0, a = 0, p = 0, s = 0):

        nonlocal used
        nonlocal edges

        if a == 0:
            edges[:] = False  # reset edges for each new patch

        used[r0, c0] = True
        a += 1

        next_r = r0 + r_offset
        next_c = c0 + c_offset
        
        foreign = data[next_r, next_c] != data[r0, c0]
        p += sum(foreign)

        # add edges & counter-edges
        for d in np.nonzero(foreign)[0]:
            edges[r0, c0, d] = True
            edges[next_r[d], next_c[d], d ^ 1] = True

        # figure out if new edge creates/continues/deletes sides
        def side_count(direction, neighbors):

            nonlocal s
            nonlocal edges

            if not foreign[direction]:
                return

            # check if neighbors share edge
            extensions = sum(edges[next_r[neighbors], next_c[neighbors], direction])

            if extensions == 0:    # edge creates new side
                    s += 1
            elif extensions == 2:  # edge merges two existing sides
                s -= 1  

            # check if next cell shares perpendicular edges
            crossings = sum(
                edges[next_r[direction], next_c[direction], neighbors] & \
                edges[r0, c0, neighbors])

            s += crossings # each crossing breaks 1/2 existing sides

        side_count(UP, [LEFT, RIGHT])
        side_count(DOWN, [LEFT, RIGHT])
        side_count(LEFT, [UP, DOWN])
        side_count(RIGHT, [UP, DOWN])

        heads = ~used[next_r, next_c] & ~foreign
        hr, hc = next_r[heads], next_c[heads]
        used[hr, hc] = True

        for r, c in zip(hr, hc):
            a, p, s = grow(r, c, a, p, s)

        return a, p, s
    
    regions = []
    seed = (1,1)
    while seed:
        r0, c0 = seed
        a, p, s = grow(r0, c0)
        regions.append(Region(data[r0, c0], a, p, s))
        seed = next_seed(used)

    return sorted(regions, key=lambda r: r.tag)


def main(file=None, part=[1,2]):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    data = np.array([list(line.strip()) for line in lines])

    regions = find_regions(data)

    totals = [sum(r.area*r.perimeter for r in regions),
              sum(r.area*r.sides for r in regions)]

    if isinstance(part, list):
        return [totals[p-1] for p in part]
    else:
        return totals[part-1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_args()
    totals = main(args.file)
    for part, total in zip(args.part, totals):
        print(f'Part {part} total: {total}')
