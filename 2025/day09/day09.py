#! /usr/bin/env python3
"""
Advent of Code 2025, day 9
https://adventofcode.com/2025/day/9
"""

import argparse
from pathlib import Path

import numpy as np
from matplotlib.path import Path as Polygon


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


def largest_rectangle(coords: np.array) -> int:

    assert coords.shape[1] == 2
    triu = np.triu_indices(coords.shape[0], 1)
    areas = (
        np.prod(np.abs(coords[a] - coords[b]) + 1) for a, b in zip(triu[0], triu[1])
    )

    return max(areas)


def largest_colored_rectangle(coords: np.array) -> int:

    assert coords.shape[1] == 2

    # shrink spans between coordinates
    ncoords = np.zeros_like(coords)
    _, ncoords[:, 0] = np.unique(coords[:, 0], return_inverse=True)
    _, ncoords[:, 1] = np.unique(coords[:, 1], return_inverse=True)

    size = np.max(ncoords, axis=0) + 1
    grid = np.meshgrid(range(0, size[0]), range(0, size[1]))
    grid = np.column_stack((grid[0].flatten(), grid[1].flatten()))

    colored = Polygon(ncoords).contains_points(grid, radius=0.5)

    # sort all possible rectangles by descending area
    triu = np.triu_indices(coords.shape[0], 1)
    pairs = list(zip(triu[0], triu[1]))
    pairs.sort(key=lambda x: -np.prod(np.abs(coords[x[1]] - coords[x[0]]) + 1))

    for j, (a, b) in enumerate(pairs):

        if j % 1000 == 0:
            print(f"Testing rectangle {j}/{len(pairs)}")

        r = np.vstack((ncoords[a], ncoords[b]))
        in_rectangle = np.all(
            np.logical_and(grid >= np.min(r, axis=0), grid <= np.max(r, axis=0)), axis=1
        )
        if all(colored[in_rectangle]):
            return np.prod(np.abs(coords[a] - coords[b]) + 1)


def color_grid_points(ncoords: np.array):

    assert np.all(ncoords >= 0)

    size = np.max(ncoords, axis=0) + 1
    xv, yv = np.meshgrid(range(0, size[0]), range(0, size[1]))
    p = Polygon(ncoords)
    flags = p.contains_points(np.column_stack((xv.flatten(), yv.flatten())), radius=0.5)

    return flags.reshape(size)


def main(file=None, part=None, verbose=False, n=1000):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    coords = np.array([np.fromstring(line, dtype=int, sep=",") for line in lines])

    if part == 1:
        total = largest_rectangle(coords)
    elif part == 2:
        total = largest_colored_rectangle(coords)
    else:
        raise ValueError(f"Invalid part number: {part}")

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
