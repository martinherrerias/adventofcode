#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from collections import deque

import numpy as np

ROBOT = '@'
BOX_SINGLE = 'O'
BOX_LEFT  = '['
BOX_RIGHT = ']'
SPACE = '.'
WALL = '#'

class Warehouse:
    def __init__(self, file, double_width = False):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        def _double(line):
            return line.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')

        if double_width:
            self.wh = np.array([list(_double(r.strip())) for r in lines if r[0] == WALL])
        else:
            self.wh = np.array([list(r.strip()) for r in lines if r[0] == WALL])

        moves = ''.join([r.strip() for r in lines if r[0] != WALL])
        self.moves_left = deque(moves)

        r, c = np.nonzero(self.wh == ROBOT)
        assert r.size == 1 and c.size == 1
        self.robot = (r[0], c[0])

        self.is_double_width = double_width


    def move(self):

        r, c = self.robot
        direction = self.moves_left.popleft()

        if direction == '>':
            c += move_in_row(self.wh[r,c:])
        elif direction == '<':
            c -= move_in_row(self.wh[r,:c+1], reverse=True)

        elif self.is_double_width:
            if direction == '^':
                r -= self._push_double_boxes(offset=-1)
            elif direction == 'v':
                r += self._push_double_boxes(offset=1)
        else:
            if direction == '^':
                r -= move_in_row(self.wh[:r+1,c], reverse=True)
            elif direction == 'v':
                r += move_in_row(self.wh[r:,c])

        self.robot = (r, c)

        return self

    def _push_double_boxes(self, offset):

        r0, c0 = self.robot
        pushed = np.zeros(self.wh.shape[1], dtype=bool)

        r, c = r0, np.array(c0)
        boxes = []
        for _ in range(self.wh.shape[0]):
            
            r = r + offset
            
            if np.any(self.wh[r,c] == WALL): # whole thing is blocked
                return False
            
            if np.all(self.wh[r,c] == SPACE): # free to move
                break

            pushed[:] = False
            
            c_left = self.wh[r,c] == BOX_LEFT
            if np.any(c_left):
                pushed[c[c_left]] = True
                pushed[c[c_left]+1] = True

            c_right = self.wh[r,c] == BOX_RIGHT
            if np.any(c_right):
                pushed[c[c_right]] = True
                pushed[c[c_right]-1] = True

            if any(pushed):
                c = np.nonzero(pushed)[0]
                boxes.extend([(r,c) for c in c])
            else:
                break

        if any(boxes):
            r, c = zip(*boxes)
            next_r = [r + offset for r in r]
            contents = self.wh[r,c].copy()
            self.wh[r,c] = SPACE
            self.wh[next_r,c] = contents
        
        self.wh[r0,c0] = SPACE
        self.wh[r0+offset,c0] = ROBOT

        return True

    def dance(self):
        while self.moves_left:
            self.move()

    def score(self):
        if self.is_double_width:
            r, c = np.nonzero(self.wh == BOX_LEFT)
        else:
            r, c = np.nonzero(self.wh == BOX_SINGLE)
        return sum([r*100 + c for r,c in zip(r,c)])

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.wh) + \
            f'\nmoves left: {"".join(self.moves_left)}'


def move_in_row(row: np.array, reverse=False):
    """
    Modify row (np.array of characters) in place: @[]..# -> .@[].#
    If reverse: #..[]@ -> #.[]@.
    """

    idx = np.nonzero((row == SPACE) | (row == WALL))[0]

    start = 0 - reverse
    assert row[start] == ROBOT
    if row[idx[start]] == WALL:
        return False
    row[start] = SPACE
    
    if reverse:
        row[idx[-1]:-2] = row[idx[-1]+1:-1]
        row[-2] = ROBOT
    else:
        row[2:idx[0]+1] = row[1:idx[0]]
        row[1] = ROBOT
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

    if part == 1:
        wh = Warehouse(file)
        wh.dance()
        return wh.score()
    elif part == 2:
        wh = Warehouse(file, double_width=True)
        wh.dance()
        return wh.score()
    else:
        raise ValueError(f'Invalid part number: {part}')


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
