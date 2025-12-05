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


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    ranges = [tuple(map(int, s.strip().split("-"))) for s in lines if "-" in s]
    ingredients = np.array(
        [int(s.strip()) for s in lines if s.strip() and "-" not in s]
    )

    if part == 1:
        values = fresh_ingredients(ingredients, ranges)
    elif part == 2:
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid part number: {part}")

    total = len(values)

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
