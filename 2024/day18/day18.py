#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from collections import namedtuple

from scipy.sparse import dok_array
from scipy.sparse.csgraph import shortest_path

import numpy as np

HEADINGS = [(0,1), (-1,0), (0,-1), (1,0)]

Node = namedtuple('Node', ['row', 'col'])

class Maze2:
    def __init__(self, file, size):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        self.coords = np.vstack([np.fromstring(x, sep=',', dtype=int) for x in lines])

        assert max(self.coords[:,0]) <= size[0]
        assert max(self.coords[:,1]) <= size[1]

        self.size = size
        self.start = Node(0, 0)
        self.end = Node(size[0]-1, size[1]-1)

    def _graph(self, t):

        isobs = np.zeros(self.size, dtype=bool)
        isobs[self.coords[0:t,0], self.coords[0:t,1]] = True

        nodes = [Node(r,c) for r,c in zip(*np.nonzero(~isobs))]
        node_idx = {n: i for i, n in enumerate(nodes)}

        n_nodes = len(nodes)
        graph = dok_array((n_nodes, n_nodes), dtype=np.uint16)

        for i, (r, c) in enumerate(nodes):

            for h in HEADINGS:
                n = Node(r + h[0], c + h[1])
                if (0 <= n[0] < self.size[0]) and \
                   (0 <= n[1] < self.size[1]) and \
                    not isobs[n[0], n[1]]:

                    graph[i, node_idx[n]] = 1

        return graph, node_idx

    def solve(self, t):

        graph, node_idx = self._graph(t)

        start = node_idx[self.start]
        end = node_idx[self.end]

        dist_from_start = shortest_path(csgraph=graph,
                                        directed=False, indices=start)
        best = dist_from_start[end]

        return int(best) if ~np.isinf(best) else None

    def first_unsolvable(self, t0 = 0):

        a = t0
        b = len(self.coords)

        assert self.solve(a) is not None
        assert self.solve(b) is None

        while b - a > 1:
            t = (a + b) // 2
            if self.solve(t) is None:
                b = t
            else:
                a = t

        return tuple(self.coords[a])

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'),
        help='Input file, default: %(default)s')
    parser.add_argument('--size', type=int, nargs=2, default=(71,71),
        help='Size of the maze, default: %(default)s')
    parser.add_argument('--t0', type=int, default=1024,
        help='Initial number of obstacles, default: %(default)s')
    return parser.parse_args()

def main(file, size, t0):

    mz = Maze2(file, size)
    return mz.solve(t=t0), mz.first_unsolvable(t0)

if __name__ == '__main__':
    args = parse_args()
    p1, p2 = main(args.file, args.size, args.t0)
    print(f'Part 1: {p1}, Part 2: {p2}')
