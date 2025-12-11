#! /usr/bin/env python3
"""
Advent of Code 2025, day 11
https://adventofcode.com/2025/day/11
"""

import argparse
from pathlib import Path

from graphlib import TopologicalSorter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=Path(__file__).with_suffix(".dat"),
        help="Input file, default: %(default)s",
    )
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        nargs="+",
        default=[1, 2],
        help="Part number(s), default: %(default)s",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def count_paths(graph, start, end):
    """
    Calculate the number of paths from start to end
    """

    node_order = list(TopologicalSorter(graph).static_order())
    node_order.reverse()

    ways = {k: 0 for k in node_order}
    ways[start] = 1
    for node in node_order[node_order.index(start):node_order.index(end) + 1]:
        for neighbor in graph.get(node, []):
            ways[neighbor] += ways[node]

    return ways[end]


def read_graph(rows):

    graph = {}
    for r in rows:
        a, b = r.split(':')
        assert graph.get(a) is None
        graph[a] = b.strip().split(' ')

    return graph


def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    graph = read_graph(lines)

    if part == 1:
        total = count_paths(graph, 'you', 'out')
    elif part == 2:
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid part number: {part}")

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
