#! /usr/bin/env python3

'''
Advent of Code 2023 - Day 3: Gear Ratios
Part 1. Find the sum of all numbers that are adjacent to a symbol
Part 2. Find the sum of products of all _pairs_ of numbers adjacent to a *
'''

import sys
import re
import argparse
import numpy as np

def adjacent(x_start, x_end, y_start, y_end, n):
        
    xc = (x_start + x_end)/2
    yc = (y_start + y_end)/2
    adjacent_rows = (abs(xc // n - yc // n) <= 1)

    m = ((x_end - x_start) + (y_end - y_start))/2 + 1
    d = abs(yc - xc) % n
    d[d > n/2] -= n 
    adjacent_cols = (abs(d) <= m)

    return adjacent_rows & adjacent_cols

def main():

    parser = argparse.ArgumentParser(usage='cat data.txt | dayX.py [-v] [--part 1]')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    args = parser.parse_args()

    lines = sys.stdin.readlines()

    # Get the length of the first line in sys.stdin
    n = len(lines[0].strip())
    if args.verbose:
        print('columns: ', n)

    # Join lines into a sigle string, replace new-lines with an extra dot
    lines = ''.join(lines).replace('\n', '.')
    n += 1

    # Find all numbers in all rows of sys.stdin
    matches = list(re.finditer(r'\d+', lines, re.DOTALL))

    # Get the start index, end index, and value of each number
    digit_starts = np.array([digit.start() for digit in matches]) + 1
    digit_ends = np.array([digit.end() for digit in matches])
    digits = np.array([int(digit.group(0)) for digit in matches])

    # Find all symbols/'*' in all rows of sys.stdin
    if args.part == 1:
        matches = list(re.finditer(r'[^\.\d]', lines, re.DOTALL))
    else:
        matches = list(re.finditer(r'\*', lines, re.DOTALL))

    symbol_idx = np.array([symbol.start() for symbol in matches]) + 1
    symbols = np.array([symbol.group(0) for symbol in matches])

    # just checking
    symbol_ends = np.array([symbol.end() for symbol in matches])
    assert all(symbol_idx == symbol_ends), "Symbol starts and ends do not match"

    if args.verbose:
        print('digit_values:', digits)
        print('digit_starts:', digit_starts)
        print('digit_ends:', digit_ends)
        print('symbol_idx:', symbol_idx)
        print()

    total = 0
    if args.part == 1:
        for start, end, value in zip(digit_starts, digit_ends, digits):
            valid = adjacent(start, end, symbol_idx, symbol_idx, n)

            if any(valid):
                total += value
                if args.verbose:
                    print(f'{value}: symbol(s) {symbols[valid]} in range')
            elif args.verbose:
                print(f'{value}: no symbols found within range')   
    else:
        for idx, sym in zip(symbol_idx, symbols):
            valid = adjacent(idx, idx, digit_starts, digit_ends, n)

            if sum(valid) == 2:  
                total += np.prod(digits[valid])
                if args.verbose:
                    print(f'{sym}@{idx}: {digits[valid]} in range, product = {np.prod(digits[valid])}')
            elif args.verbose:
                print(f'{sym}@{idx}: {digits[valid]} in range (not two!)')     
 
    print(f'Score: {total}')

if __name__ == '__main__':
    main()

