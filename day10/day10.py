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

    t = tiles[i][j]
    if i > 0 and t.N and tiles[i-1][j].S:
        yield (i-1, j)
    if i < len(tiles)-1 and t.S and tiles[i+1][j].N:
        yield (i+1, j)
    if j > 0 and t.W and tiles[i][j-1].E:
        yield (i, j-1)
    if j < len(tiles[0])-1 and t.E and tiles[i][j+1].W:
        yield (i, j+1)

def get_path(tiles):

    start = next((i, j) for i, row in enumerate(tiles) for j, tile in enumerate(row) if tile.key == 'S')
    path = [start]

    c = list(connections(tiles, *start))
    assert len(c) == 2

    tile = c[0]
    while tile != start:

        path.append(tile)

        c = list(connections(tiles, *tile))
        assert len(c) == 2

        if c[0] == path[-2]:
            tile = c[1]
        else:
            tile = c[0]
        
    return path

def get_distances(tiles, verbose=False):

    path = get_path(tiles)

    D = np.zeros((len(tiles), len(tiles[0])), dtype=int)
    D.fill(-1)

    for idx, (i, j) in enumerate(path):
        d = min(idx, len(path)-idx)
        D[i,j] = d
    
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

