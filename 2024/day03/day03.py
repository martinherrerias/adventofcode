#! /usr/bin/env python3

'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import sys
import argparse
import re
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        usage=f'python3 {Path(__file__).name} [--file DATA] [--part N] [-v]'
              f'cat DATA | {Path(__file__).name} [--part 1] [-v]'
    )
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat').name, 
        help='Specify input file, default: %(default)s')
    parser.add_argument('--part', type=int, default=1, help='Part number, default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    return parser.parse_args()

def part_1(row):
    match = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', row)
    value = 0
    for m in match:
        value += int(m[0]) * int(m[1])
    return value

def part_2(row):

    assert '\n' not in row  # arghhh

    chunks = row.split("don't()")
    chunks[0] = 'do()' + chunks[0]

    value = 0
    for c in chunks:
        c = re.sub(r'^.*?do\(\)', r'', c + 'do()', count=1)
        value += part_1(c)
    return value

def main(file=None, part=None, verbose=False):

    if file:
        with open(file, encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    lines = [l.strip() for l in lines]
    text = ''.join(lines)

    if part == 1:
        total =part_1(text)
    elif part == 2:
        total = part_2(text)
    else:
        raise ValueError(f'Invalid part number: {part}')
    
    return total

if __name__ == '__main__':
    args = parse_args()
    total = main(**vars(args))
    print(f'Score: {total}')
