#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path

import numpy as np
import re
from graphlib import TopologicalSorter

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def test_sequence(rules, sequence, fix = False):

    # Remove irrelevant rules
    relevant = np.isin(rules[0], sequence) & np.isin(rules[1], sequence)
    rules = [np.array(r)[relevant] for r in rules]

    # Check for inconsistencies
    bad = False
    for j, k in zip(rules[0], rules[1]):
        if np.where(sequence == j)[0] > np.where(sequence == k)[0]:
            bad = True
            break

    if bad and fix:
        # Part 2: correct bad sequences
        order = sorter(rules)
        assert all(np.isin(sequence, order))
        sequence = order

    if (not bad and fix) or (bad and not fix):
        return 0
    else:
        return sequence[len(sequence) // 2]


def sorter(rules):

    graph = {}
    for j, k in zip(rules[0], rules[1]):
        if k not in graph:
            graph[k] = []
        graph[k].append(j)

    ts = TopologicalSorter(graph)
    return list(ts.static_order())


def part_1(rules, sequence):
    return test_sequence(rules, sequence, fix = False)

def part_2(rules, sequence):
    return test_sequence(rules, sequence, fix = True)


def read_input(file):
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    rules = []
    sequences = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r'(\d+)\|(\d+)', line)
        if match:
            rules.append((int(match.group(1)), int(match.group(2))))
        else:
            seq = np.fromstring(line, dtype=int, sep=',')
            assert seq.size % 2 == 1
            sequences.append(seq)

    print(f'Read {len(rules)} rules and {len(sequences)} sequences')

    # transpose list of 2-tuples, into 2-list [before, after]
    rules = [np.array(x) for x in list(zip(*rules))]

    return rules, sequences


def main(file=None, part=None, verbose=False):

    rules, sequences = read_input(file)

    if part == 1:
        values = [part_1(rules, s) for s in sequences]
    elif part == 2:
        values = [part_2(rules, s) for s in sequences]
    else:
        raise ValueError(f'Invalid part number: {part}')

    total = sum(values)
    
    if verbose:
        for s, v in zip(sequences, values):
            print(f'{s}: {v}')

    return total


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
