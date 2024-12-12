#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from math import log10
from itertools import chain

from numpy import nan

def digits(n):
    return int(log10(n))+1

def shift_stone(n):
    if n == 0:
        return [1]
    elif digits(n) % 2 == 0:
        n_str = str(n)
        return [int(n_str[:len(n_str)//2]), int(n_str[len(n_str)//2:])]
    else:
        return [n*2024]

def graph_leaves(graph):
    values = set(chain.from_iterable(graph.values()))
    return set(values) - set(graph.keys())

def blinks_graph(stones, n_blinks):
    """
    Return a graph that represents all possible transitions up to N blinks
    """

    graph = {s: shift_stone(s) for s in stones}
    for _ in range(n_blinks - 1):
        leaves = graph_leaves(graph)
        if not leaves:
            break
        for s in leaves:
            graph[s] = shift_stone(s)

    return graph

def cleanup_graph(graph):
    """
    Re-map nodes to a contiguous range, replace leaves with a single end-node
    """

    node_map = {k: i for i, k in enumerate(graph.keys())}
    
    end_node = len(graph)    
    node_map.update({k: end_node for k in graph_leaves(graph)})

    graph = {node_map[k]: [node_map[j] for j in v] for k,v in graph.items()}
    graph[end_node] = []

    return graph, node_map

def count_paths(graph, n_steps):
    """
    Calculate the number of n_step transition paths starting from each node,
    use nan for paths beyond the end node.
    """

    paths = {k: len(v) if v else nan for k,v in graph.items()}

    for _ in range(n_steps-1):
        heads = paths
        paths = {}
        for node, subnodes in graph.items():
            paths[node] = sum(heads[j] for j in subnodes) if subnodes else nan

    return paths

def many_blinks(data, N):

    graph = blinks_graph(data, N)
    graph, node_map = cleanup_graph(graph)
    paths = count_paths(graph, N)
    starts = [node_map[s] for s in data]
    return sum(paths[j] for j in starts)


def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    data = [int(x) for x in lines[0].split()]

    if part == 1:
        return many_blinks(data, 25)
    elif part == 2:
        return many_blinks(data, 75)
    else:
        raise ValueError(f'Invalid part number: {part}')


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
