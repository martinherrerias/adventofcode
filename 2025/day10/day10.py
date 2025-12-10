#! /usr/bin/env python3
"""
Advent of Code 2025, day 10
https://adventofcode.com/2025/day/10
"""

import re
import argparse
from pathlib import Path

import numpy as np
from scipy.optimize import LinearConstraint, milp


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


def part_1(line):
    wiring_matrix, light_diagram, _ = parse_line(line)
    return match_lights(wiring_matrix, light_diagram)


def part_2(line):
    wiring_matrix, _, joltage = parse_line(line)
    return match_joltage(wiring_matrix, joltage)


def parse_line(line: str):
    data = re.match(r"\[(.+)\] (.+) \{(.+)\}", line).groups()

    light_diagram = np.array([x == "#" for x in data[0]])
    button_schematics = [
        tuple(map(int, x.split(","))) for x in data[1].strip("()").split(") (")
    ]
    joltage = tuple(map(int, data[2].split(",")))

    wiring_matrix = np.zeros((len(light_diagram), len(button_schematics)), dtype=bool)
    for b, s in enumerate(button_schematics):
        wiring_matrix[s, b] = True

    return wiring_matrix, light_diagram, joltage


def match_lights(wiring_matrix, light_diagram):

    assert wiring_matrix.shape[0] == len(light_diagram)

    # we can flip them off the same as we flipped them on
    need_switching = light_diagram
    if not any(need_switching):
        return 0

    if wiring_matrix.shape[1] > 1:

        # Is it even doable?
        # there should be switches to flip the missing lights
        if not all(np.any(wiring_matrix[need_switching, :], axis=1)):
            return np.nan

        # steps without flipping first switch
        without_first_switch = match_lights(wiring_matrix[:, 1:], light_diagram)

        # steps if flipping first switch
        new_state = np.bitwise_xor(wiring_matrix[:, 0], light_diagram)
        with_first_switch = 1 + match_lights(wiring_matrix[:, 1:], new_state)

        return np.nanmin([without_first_switch, with_first_switch])

    elif np.all(wiring_matrix[:, 0] == light_diagram):  # flip one last switch
        return 1
    else:
        return np.nan


def match_joltage(wiring_matrix, joltage):

    assert wiring_matrix.shape[0] == len(joltage)

    c = np.ones(wiring_matrix.shape[1])
    constraints = LinearConstraint(wiring_matrix, joltage, joltage)
    integrality = np.ones_like(c) * 3

    res = milp(c, integrality=integrality, constraints=constraints)
    assert res.status == 0

    return sum(res.x)


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    if part == 1:
        values = [part_1(line) for line in lines if line.strip()]
    elif part == 2:
        values = [part_2(line) for line in lines if line.strip()]
    else:
        raise ValueError(f"Invalid part number: {part}")

    total = sum(values)

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
