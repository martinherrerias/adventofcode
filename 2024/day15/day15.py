#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from collections import deque

import numpy as np

ROBOT = '@'
BOX = 'O'
SPACE = '.'
WALL = '#'

class Warehouse:
    def __init__(self, file):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        self.wh = np.array([list(r.strip()) for r in lines if r[0] == WALL])

        moves = ''.join([r.strip() for r in lines if r[0] != WALL])
        self.moves_left = deque(moves)

        r, c = np.nonzero(self.wh == ROBOT)
        assert r.size == 1 and c.size == 1
        self.robot = (r[0], c[0])

    def move(self):

        r, c = self.robot
        direction = self.moves_left.popleft()

        if direction == '^':
            r -= move_in_row(self.wh[:r+1,c], reverse=True)
        elif direction == '>':
            c += move_in_row(self.wh[r,c:])
        elif direction == 'v':
            r += move_in_row(self.wh[r:,c])
        elif direction == '<':
            c -= move_in_row(self.wh[r,:c+1], reverse=True)

        self.robot = (r, c)

    def dance(self):
        while self.moves_left:
            self.move()

    def score(self):
        r, c = np.nonzero(self.wh == BOX)
        return sum([r*100 + c for r,c in zip(r,c)])

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.wh) + \
            f'\nmoves left: {"".join(self.moves_left)}'

def move_in_row(row: np.array, reverse=False):
    """
    Modify row (np.array of characters) in place: @O..# -> .@O.#
    If reverse: #..O@ -> #.O@.
    """

    idx = np.nonzero((row == SPACE) | (row == WALL))[0]

    start = 0 - reverse
    assert row[start] == ROBOT
    if row[idx[start]] == WALL:
        return False
    row[start] = SPACE
    
    if reverse: 
        row[-2] = ROBOT
        row[idx[-1]:-2] = BOX
    else:
        row[1] = ROBOT
        row[2:idx[0]+1] = BOX
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def main(file=None, part=None, verbose=False):

    wh = Warehouse(file)
    wh.dance()

    if part == 1:
        return wh.score()
    elif part == 2:
        return None
    else:
        raise ValueError(f'Invalid part number: {part}')


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
