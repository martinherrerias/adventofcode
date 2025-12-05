#! /usr/bin/env python3
"""
Advent of Code 2025 - https://adventofcode.com/2025/
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


def fresh_ingredients(ingredients: np.array, ranges: list[tuple]):

    in_any_range = np.zeros(len(ingredients), dtype=bool)
    for lo, hi in ranges:
        in_any_range = np.logical_or(
            in_any_range, np.logical_and(ingredients >= lo, ingredients <= hi)
        )

    return ingredients[in_any_range]


def merge_ranges(ranges: list[tuple]):

    # biggest ranges first
    ranges.sort(key=lambda x: -(x[1] - x[0]))

    merged = []
    for r in ranges:
        rids = [
            next(
                (k for k, m in enumerate(merged) if r[j] >= m[0] and r[j] <= m[1]), None
            )
            for j in range(0, 2)
        ]

        if rids[0] is not None:
            if rids[1] is not None:
                if rids[0] == rids[1]:
                    # r is already included
                    pass
                else:
                    # merge two ranges
                    new_range = tuple([merged[rids[0]][0], merged[rids[1]][1]])
                    merged[rids[0]] = new_range
                    merged.pop(rids[1])
            else:
                # extend left range
                new_range = tuple([merged[rids[0]][0], r[1]])
                merged[rids[0]] = new_range
        elif rids[1] is not None:
            # extend right range
            new_range = tuple([r[0], merged[rids[1]][1]])
            merged[rids[1]] = new_range
        else:
            # entirely new range
            merged.append(r)

    return merged


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    ranges = [tuple(map(int, s.strip().split("-"))) for s in lines if "-" in s]
    ingredients = np.array(
        [int(s.strip()) for s in lines if s.strip() and "-" not in s]
    )

    if part == 1:
        values = fresh_ingredients(ingredients, ranges)
        return len(values)
    elif part == 2:
        merged = merge_ranges(ranges)
        return sum([hi - lo + 1 for lo, hi in merged])
    else:
        raise ValueError(f"Invalid part number: {part}")


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
