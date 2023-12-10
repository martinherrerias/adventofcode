#! /usr/bin/env python3

'''
Advent of Code 2023 - Day10

'''

import sys
import argparse
import inspect
import re
import numpy as np

from collections import namedtuple

Tile = namedtuple('TileType', ['key', 'N', 'S','E','W'])
def get_tile(key):
    return {
        '|': Tile('|', True, True, False, False),  # vertical pipe
        '-': Tile('-', False, False, True, True),  # horizontal pipe
        'L': Tile('L', True, False, True, False),  # 90-degree bend (N, E)
        'J': Tile('J', True, False, False, True),  # 90-degree bend (N, W)
        '7': Tile('7', False, True, False, True),  # 90-degree bend (S, W)
        'F': Tile('F', False, True, True, False),  # 90-degree bend (S, E)
        '.': Tile('.', False, False, False, False),  # ground
        'S': Tile('S', True, True, True, True),  # starting position
    }[key]

def connections(tiles, i, j):

    assert isinstance(tiles, list)
    assert isinstance(tiles[i], list)
    assert isinstance(tiles[i][j], Tile)

    t = tiles[i][j]
    if i > 0 and t.N and tiles[i-1][j].S:
        yield (i-1, j)
    if i < len(tiles)-1 and t.S and tiles[i+1][j].N:
        yield (i+1, j)
    if j > 0 and t.W and tiles[i][j-1].E:
        yield (i, j-1)
    if j < len(tiles[0])-1 and t.E and tiles[i][j+1].W:
        yield (i, j+1)

def get_distances(tiles, verbose=False):

    assert isinstance(tiles, list)
    assert isinstance(tiles[0], list)
    assert isinstance(tiles[0][0], Tile)

    D = np.zeros((len(tiles), len(tiles[0])), dtype=int)
    D.fill(-1)
    open_ends = np.zeros((len(tiles), len(tiles[0])), dtype=bool)

    start = next((i, j) for i, row in enumerate(tiles) for j, tile in enumerate(row) if tile.key == 'S')
    D[start] = 0
    open_ends[start] = True

    if verbose:
        print(f'Starting at {start}')

    for iter in range(len(tiles) * len(tiles[0])):
        if not np.any(open_ends):
            break
        if verbose:
            print(f'Iteration {iter}')
        
        for i, j in zip(*np.where(open_ends)):
            d = D[i,j]
            c = list(connections(tiles, i, j))
            if verbose:
                print(f'Found {len(c)} connections for {tiles[i][j].key}@({i},{j}): {c}')

            for ci, cj in c:
                if D[ci,cj] == -1 or D[ci,cj] > d + 1:

                    D[ci,cj] = d + 1
                    open_ends[ci,cj] = True

                    if verbose:
                        print(f'Flagged {tiles[ci][cj].key}@({ci},{cj}) as open, with dist {d+1}')
                else:
                    open_ends[ci,cj] = False
    
    return D

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day10.py [-v] [--part 1]
        python3 -m day10.py --file data.txt [-v] [--part 1]''')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    parser.add_argument('--file', type=str, help='Specify input file')
    return parser.parse_args()

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    tiles = [[get_tile(c) for c in line.strip()] for line in lines]

    D = get_distances(tiles, args.verbose)

    total = np.max(D)

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

