#! /usr/bin/env python3
"""
Advent of Code 2025, day 8
https://adventofcode.com/2025/day/8
"""

import argparse
from pathlib import Path

import numpy as np


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


def connect_n_shortest(rows: list[np.array], n: int = 1000) -> np.array:

    triu = np.triu_indices(len(rows), 1)
    pairs = list(zip(triu[0], triu[1]))
    pairs.sort(key=lambda x: np.linalg.norm(rows[x[1]]-rows[x[0]]))

    circuits = np.array(range(0, len(rows)))
    for (a, b) in pairs[0:n]:
        circuits[circuits == circuits[b]] = circuits[a]

    return circuits


def main(file=None, part=None, verbose=False, n=1000):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    rows = [np.fromstring(line, dtype=int, sep=",") for line in lines]

    if part == 1:
        circuits = connect_n_shortest(rows, n=n)
    elif part == 2:
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid part number: {part}")

    uniq = np.unique_counts(circuits)

    if verbose:
        print(f'{len(uniq.values)} circuits, with counts: {uniq.counts}\n')
        for i, c in enumerate(circuits):
            print(f"{rows[i]}: {c}")

    largest = list(uniq.counts)
    largest.sort(reverse=True)
    total = np.prod(largest[0:3])

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
