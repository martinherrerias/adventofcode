#! /usr/bin/env python3

'''
Advent of Code 2023 - Day07
'''

import sys
import argparse
import inspect
import re
import numpy as np

CARD_VALUES = ('AKQJT98765432','AKQT98765432J')

def parse_input(line, part):

    match = re.match(r'([' + CARD_VALUES[0] + r']{5}) (\d*)', line)
    hand, bid = match.groups()

    bid = int(bid)

    # parse CARD_VALUES[0] into indices 13..1
    idx = tuple([len(CARD_VALUES[0]) - CARD_VALUES[part-1].index(i) for i in hand])

    letters = np.array(list(hand))

    # get repeated letter counts (right-padded with zeros)
    if part == 1:
        jokers = np.zeros(5, dtype=bool)
    else:
        jokers = (letters == 'J')

    letters = set(letters[~jokers])
    
    counts = [0]*5
    counts[0:len(letters)] = [hand.count(c) for c in letters]
    counts = sorted(counts, reverse=True)

    if part == 2: counts[0] += sum(jokers)

    return hand, bid, idx, tuple(counts)

def sort_index(counts, idx):

    idx = np.array(idx)
    counts = np.array(counts)
    table = np.concatenate((counts, idx), axis=1)
    sort_idx = np.lexsort(np.fliplr(table).T)

    return sort_idx

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day07.py [-v] [--part 1]
        python3 -m day07.py --file data.txt [-v] [--part 1]''')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    parser.add_argument('--file', type=str, help='Specify input file')
    return parser.parse_args()

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    hands, bids, idx, counts = zip(*[parse_input(line, args.part) for line in lines])
    sidx = sort_index(counts, idx)

    total = 0
    for i, j in enumerate(sidx):
        
        total += bids[j] * (i + 1)
        if args.verbose:
            print(f'{i}. {hands[j]} {bids[j]}')

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

