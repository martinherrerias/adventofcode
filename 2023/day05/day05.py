#! /usr/bin/env python3

'''
Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer
'''

import sys
import re
import argparse
import numpy as np
import inspect

from collections import namedtuple

Rule = namedtuple('Rule', ['src', 'tgt', 'tgt_start', 'src_start', 'rng_len'])

def read_input(lines, seeds, part, verbose = False):

    if seeds:
        seeds = np.array(seeds)
        if verbose: print(f'\nSeeds (override): {seeds}')
    else:
        # Read seeds
        seeds = re.findall(r'(\d+)', lines[0])
        seeds = np.array(list(map(int, seeds)))

    if part == 2:
        seed_specs = seeds
        seeds = [(i,i+r-1) for i,r in zip(seed_specs[0::2], seed_specs[1::2])]
        if verbose: print(f'\nSeeds: {seed_specs} >> {seeds}')
    else:
        if verbose: print(f'\nSeeds: {seeds}')

    lines = '\n'.join(lines)

    # Parse maps
    if verbose: print(f'\nMaps:')
    matches = list(re.finditer(r'(\w*)-to-(\w*) map:([\d\s\n]*)', lines, re.DOTALL))
    rules = [parse_rule(match, verbose) for match in matches]

    # Just check that the rules are in the right order
    tgt = 'seed'
    for rule in rules:
        assert tgt == rule.src, f'Current target {tgt} != map source {rule.src}'
        tgt = rule.tgt
    assert tgt == 'location'

    return seeds, rules

def parse_rule(match, verbose=False):
    
    src = match.group(1)
    tgt = match.group(2)

    digits = [int(digit) for digit in match.group(3).strip().split()]

    tgt_start = np.array(digits[0::3])
    src_start = np.array(digits[1::3])
    rng_len = np.array(digits[2::3])

    if verbose:
        print(f'\n  {src}-{tgt}: [target] [source] [range]')
        for s, t, r in zip(src_start, tgt_start, rng_len):
            print(f'\t{t} {s} {r}')

    return Rule(src, tgt, tgt_start, src_start, rng_len)

def reverse(rule):
    
        src, tgt, tgt_start, src_start, rng_len = rule
        return Rule(tgt, src, src_start, tgt_start, rng_len)

# Break down interval into tuples that do not contain any breaks, except:
#   (possibly) at the start, if are_starts
#   (possibly) at the end, if !are_starts   
def intersect(interval, breaks, are_starts):

    if isinstance(interval, list):
        broken = []
        for i in interval:
            ii = intersect(i, breaks, are_starts)
            if not isinstance(ii, list): ii = [ii]
            broken.extend(ii)
        return broken
    
    assert isinstance(interval, tuple) and len(interval) == 2
    breaks = np.atleast_1d(np.unique(breaks))

    if are_starts:
        inside = (breaks > interval[0]) & (breaks <= interval[1])
    else:
        inside = (breaks >= interval[0]) & (breaks < interval[1])

    if any(inside):
        broken = []
        x0 = interval[0]
        for b in breaks[inside]:
            broken.append((x0, b - 1) if are_starts else (x0, b))
            x0 = b if are_starts else b + 1
        broken.append((x0, interval[1]))
    else:
        broken = tuple(interval)

    return broken

def map_numbers(rule, numbers, verbose=False):

    if isinstance(numbers, list): 
        mapped = [ map_numbers(rule, x, verbose) for x in numbers ]
        return mapped
    
    numbers = np.array(numbers)
    mapped = np.array(numbers)

    for s, t, rng in zip(rule.src_start, rule.tgt_start, rule.rng_len):
        d = numbers - s
        in_range = (d >= 0) & (d < rng)
        if any(in_range):
            mapped[in_range] = t + d[in_range]

    if verbose:
        print(f'{rule.src}: {numbers} >> {rule.tgt}: {mapped}')
    
    return mapped

def map_intervals(rule, interval, verbose=False):

    mapped = intersect(interval, rule.src_start, True)
    mapped = intersect(mapped, rule.src_start + rule.rng_len - 1, False)
    mapped = [ tuple(map_numbers(rule, r, verbose)) for r in mapped ]

    if verbose:
       print(f'{rule.src}-{rule.tgt}: {interval} >> {mapped}\n')

    return mapped

def traceback(value, rules, verbose):

    origin = (value, value)
    for rule in rules[::-1]:
        origin = map_intervals(reverse(rule), origin, verbose)

    return(origin[0])

def parse_args():
    parser = argparse.ArgumentParser(usage='cat data.txt | dayX.py [-v] [--part 1]')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    parser.add_argument('--file', type=str, help='Specify input file')
    parser.add_argument('--seeds', type=int, nargs='+', help='Override seeds (debugging)')
    return parser.parse_args()

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    seeds, rules = read_input(lines, args.seeds, args.part, args.verbose)

    if args.verbose: print()

    mapped = seeds

    if isinstance(seeds[0], tuple):
        for rule in rules:
            mapped = map_intervals(rule, mapped, args.verbose)
    else:
        for rule in rules:
            mapped = map_numbers(rule, mapped, args.verbose)

    best = min(np.array(mapped).flatten())
    
    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return best
    else:
        print(f'Lowest location: {best}')

if __name__ == '__main__':
    args = parse_args()
    main(args)