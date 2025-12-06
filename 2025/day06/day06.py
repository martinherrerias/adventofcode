#! /usr/bin/env python3
"""
Advent of Code 2025 - https://adventofcode.com/2025/
"""

import argparse
from pathlib import Path
import re

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


def do_op(op, numbers):
    fn = {"+": np.sum, "*": np.prod}[op]
    return fn(numbers)


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    operations = re.split(r"\s+", lines.pop(-1).strip())
    numbers = np.array(
        [np.fromstring(line, dtype=int, sep=" ") for line in lines]
    ).transpose()

    if part == 1:
        values = [do_op(op, nm) for op, nm in zip(operations, numbers)]
    elif part == 2:
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid part number: {part}")

    total = sum(values)

    if verbose:
        for i, (op, nm, v) in enumerate(zip(operations, numbers, values)):
            print(f"{i}: {op} {nm} = {v}")

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
