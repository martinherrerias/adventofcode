#! /usr/bin/env python3

'''
Advent of Code 2023 - Day 2: Cube Conundrum
Parse a series of lines: Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Part 1: Check that the number of each color is less than the max, if so, return the game ID
Part 2: Multiply the min. required number of each color
'''

import sys
import re
import argparse

def check_game(line, rgb, part=2):
    
    if part == 1:
        msg = 'ok'
        out = int(re.match(r'Game (\d*):', line).group(1))
    else:
        msg = 'power = '
        out = 1

    for color in ['red', 'green', 'blue']:
        
        match = re.findall(f'(\d*) {color}', line)
        if any(match):
            val = max(map(int, match))
        else:
            val = 0

        if part == 1:
            if val > rgb[color]:
                out = 0
                msg = f'{val} > {rgb[color]} {color}!'
                break
        else:
            out *= val
            msg += f'({val})'

    if part == 1:
        if out > 0:
            msg = f'ok (ID = {out})'
    elif part == 2:
        msg += f' = {out}'

    return out, msg

def main():

    parser = argparse.ArgumentParser(usage='cat day02.txt | day02.py [-v] [--part 1 --rgb 12 13 14]')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    parser.add_argument('--rgb', type=int, nargs=3, default=[12, 13, 14], help='Max number of each color')
    args = parser.parse_args()

    args.rgb = dict(zip(['red', 'green', 'blue'], args.rgb))

    total = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        value, msg = check_game(line, args.rgb, args.part)
        total += value
        if args.verbose:
            print(f'{line} >> {msg}')

    print(f'Score: {total}')

if __name__ == '__main__':
    main()

