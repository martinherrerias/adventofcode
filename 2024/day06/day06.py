#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path

import numpy as np

OBSTACLE = '#'
NEW_OBSTACLE = 'O'
START = '^'
FILLER = 'X'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def start(data):
    r, c = np.nonzero(data == START)
    assert r.size == 1 and c.size == 1
    return r[0], c[0]

def move(row, reverse=False):
    """
    Replace characters in `row` with FILLER, up to the first OBSTACLE.
    If `reverse` is True, replace characters after the last OBSTACLE.
    Return the modified row and the number of characters replaced.
    """
    idx = np.nonzero(row == OBSTACLE)[0]
    if not len(idx) > 0:
        row[:] = FILLER
        return row, len(row)
    if reverse:
        row[idx[-1]+1:] = FILLER
        return row, len(row) - idx[-1] - 2
    else:
        row[:idx[0]] = FILLER
        return row, idx[0]-1

def trace_path(data, new_obstacle=None):
    """
    Trace a path through the grid replacing characters with FILLER, until an
    edge is reached or a loop is detected.
    If `new_obstacle`=(row, col), place an additional OBSTACLE at that point.
    """

    r0, c0 = start(data)
    direction = START
    r, c = r0, c0

    walked = data.copy()
    if new_obstacle is not None:
        walked[new_obstacle] = OBSTACLE

    visited = []
    caught_in_loop = False
    while 0 <= r < walked.shape[0] and 0 <= c < walked.shape[1]:

        if (r,c,direction) in visited:
            caught_in_loop = True
            break
        else:
            visited.append((r,c,direction))

        if direction == '^':
            walked[:r+1,c], moved = move(walked[:r+1,c], reverse=True)
            r -= moved
            direction = '>'
        elif direction == '>':
            walked[r,c:], moved = move(walked[r,c:])
            c += moved
            direction = 'v'
        elif direction == 'v':
            walked[r:,c], moved = move(walked[r:,c])
            r += moved
            direction = '<'
        elif direction == '<':
            walked[r,:c+1], moved = move(walked[r,:c+1], reverse=True)
            c -= moved
            direction = '^'

    # (re)mark the starting point [and obstruction], for display
    walked[r0,c0] = START
    if new_obstacle is not None:
        walked[new_obstacle] = NEW_OBSTACLE

    return walked, caught_in_loop

def print_mat(title, data):
    print(f'\n{title}:')
    for row in data:
        print(' '.join(row))

def part_1(data, verbose=False):
    walked, is_loop = trace_path(data)
    if verbose:
        print_mat('Walked', walked)
    assert not is_loop
    return np.sum(walked==FILLER) + 1


def part_2(data, verbose=False):

    walked, is_loop = trace_path(data)
    assert not is_loop

    # obstruction has to be somewhere in the original path
    path = np.nonzero(walked == FILLER)

    if verbose:
        print_mat('data', data)

    loop_count = 0
    for i,j in zip(*path):

        walked, is_loop = trace_path(data, new_obstacle=(i,j))        
        if is_loop:
            loop_count += 1
            if verbose:
                print_mat(f'Obstruction at {i},{j}', walked)

    return loop_count


def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    data = np.array([list(line.strip()) for line in lines])

    if part == 1:
        total = part_1(data, verbose)
    elif part == 2:
        total = part_2(data, verbose)
    else:
        raise ValueError(f'Invalid part number: {part}')

    return total


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
