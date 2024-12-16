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

START = 'S'
END = 'E'
WALL = '#'

HEADINGS = [(0,1), (-1,0), (0,-1), (1,0)]
START_HEADING = 0

TURN_COST = 1000
MOVE_COST = 1

Node = namedtuple('Node', ['row', 'col', 'heading'])

class Maze:
    def __init__(self, file):
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        self.map = np.array([list(r.strip()) for r in lines])

        r, c = np.nonzero(self.map == START)
        assert r.size == 1 and c.size == 1
        self.start = Node(r[0], c[0], START_HEADING)

        r, c = np.nonzero(self.map == END)
        assert r.size == 1 and c.size == 1
        self.ends = [Node(r[0], c[0], h) for h in range(4)]


    def graph(self):
        """
        Represent the maze as a graph over (row, col, heading) states
        """

        nodes = [Node(r,c,h) for h in range(4)
                 for r,c in zip(*np.nonzero(self.map != WALL))]

        node_idx = {n: i for i, n in enumerate(nodes)}

        n_nodes = len(nodes)
        graph = dok_array((n_nodes, n_nodes), dtype=np.uint16)

        for i, (r, c, h) in enumerate(nodes):

            # turn-left/right transitions
            graph[i, node_idx[Node(r, c, (h + 1) % 4)]] = TURN_COST
            graph[i, node_idx[Node(r, c, (h - 1) % 4)]] = TURN_COST

            # move-forward transition
            nr, nc = r + HEADINGS[h][0], c + HEADINGS[h][1]
            if self.map[nr, nc] != WALL:
                graph[i, node_idx[Node(nr, nc, h)]] = MOVE_COST

        return graph, node_idx


    def solve(self, verbose = False):

        graph, node_idx = self.graph()

        start = node_idx[self.start]
        ends = [node_idx[n] for n in self.ends]

        # Find lowest cost path
        dist_from_start = shortest_path(csgraph=graph, 
                                        directed=True, indices=start)
        best = min(dist_from_start[ends])

        # Find all nodes along paths with cost == best
        dist_from_ends = shortest_path(csgraph=graph.transpose(),
                                       directed=True, indices=ends)
        in_best_path = np.zeros(len(node_idx), dtype=bool)
        for j in range(len(ends)):
            in_best_path |= (dist_from_start + dist_from_ends[j,:] == best)

        best_nodes = [n for n, b in zip(node_idx.keys(), in_best_path) if b]
        rc = np.unique(np.vstack(best_nodes)[:,0:2], axis=0)

        if verbose:
            self.map[rc[:,0], rc[:,1]] = 'O'
            print(self)

        return int(best), rc.shape[0] 


    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.map)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def main(file=None, verbose=False):

    lab = Maze(file)
    return lab.solve(verbose=verbose)

if __name__ == '__main__':
    args = parse_args()
    p1, p2 = main(args.file, args.verbose)
    print(f'Part 1: {p1}, Part 2: {p2}')
