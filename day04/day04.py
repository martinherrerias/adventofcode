#! /usr/bin/env python3

'''
Advent of Code 2023 - Day 4: Scratchcards
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
'''

import sys
import re
import argparse

def scratch(line, verbose = False):

    line = line.strip()
    if not line:
        return(0)

    # Parse string: Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    match = re.match(r'Card\s+(\d*): ([ \d]*) \| ([ \d]*)', line)
    id = int(match.group(1))
    winning = list(map(int, match.group(2).split()))
    numbers = list(map(int, match.group(3).split()))

    winning_numbers = [n for n in numbers if n in winning]

    return len(winning_numbers)

def main():

    parser = argparse.ArgumentParser(usage='cat data.txt | template.py [-v] [--part 1]')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    args = parser.parse_args()

    lines = sys.stdin.readlines()
    n_winning_numbers = [scratch(line) for line in lines]

    total = 0
    cards = [1]*len(n_winning_numbers)

    for idx, n in enumerate(n_winning_numbers):
        if args.part == 1:
            
            value = 0 if n == 0 else 2**(n-1)
            total += value

            if args.verbose:
                print(f'{lines[idx].strip()} >> {n} winners ({value})')
        else:

            total += cards[idx]

            if n > 0:
                for i in range(idx+1, idx+n+1):
                    cards[i] += cards[idx]

            if args.verbose:
                print(f'{lines[idx].strip()} (x {cards[idx]}) >> ({n}) +{cards[idx]} to {list(range(idx+2,idx+n+2))}')

    print(f'Score: {total}')

if __name__ == '__main__':
    main()

