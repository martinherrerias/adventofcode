#! /usr/bin/env python3

'''
Advent of Code 2023 - Day12

'''

import sys
import argparse
import inspect
import numpy as np
import re
import itertools
from math import comb

def check_line(line, groups):
    pattern = match_pattern(groups)
    return pattern.match(line) is not None

def match_pattern(groups, flexible = True):
    if flexible:
        pattern = '[^#]*'
        for g in groups:
            pattern += f'(?<!#)([#?]{{{g}}})(?!#)[^#]*'
    else:
        pattern = [f'(#{{{g}}})' for g in groups]
        pattern = '\.*' + ('\.+'.join(pattern)) + '\.*'

    return re.compile(pattern)

def stats(record, groups):
    unknown = np.where(record == '?')[0]
    damaged = np.sum(record == '#')
    missing = sum(groups) - damaged
    return unknown, missing

# Check each position to see if # or . breaks the match
def check_positions(record, groups, verbose = False):

    record = np.array(list(record))
    pattern = match_pattern(groups)

    unknown, missing = stats(record, groups)
    if missing == 0:
        record[unknown] = '.'
        return record
    elif missing == len(unknown):
        record[unknown] = '#'
        return record

    def check_invalid(stuff):

        nonlocal record
        nonlocal unknown

        invalid = np.zeros(len(record), dtype=bool)
        for i in unknown:
            test = record.copy()
            test[i] = stuff
            invalid[i] = pattern.match(''.join(test)) is None

        if np.any(invalid):
            not_stuff = '.' if stuff == '#' else '#'
            record[invalid] = not_stuff
            unknown = np.where(record == '?')[0]

        return invalid
    
    invalid = True
    while np.any(invalid):
        invalid = check_invalid('#')
        invalid = check_invalid('.')

    return record

def exhaustive(record, groups):

    record = np.array(list(record))
    assert isinstance(groups, list)
    
    unknown, missing = stats(record, groups)
    pattern = match_pattern(groups, flexible = False)
    nopts = 0
    for idx in itertools.combinations(unknown, missing):
        test = record.copy()
        test[unknown] = '.'
        test[np.array(idx, dtype=int)] = '#'
        if pattern.match(''.join(test)) is not None:
            nopts += 1
    return nopts

def parse_line(line, part, verbose = False, debug = False):

    debug = verbose or debug

    groups = list(map(int, re.findall(r'(\d+)', line)))
    record = re.match(r'^[?.#]+', line).group(0)

    if part == 2:
        groups = groups*5
        record = '?'.join([record]*5)

    if verbose:
        unknown, missing = stats(record, groups)
        print(f'raw: ' + ''.join(record) + f': {missing} missing # in {len(unknown)} gaps')

    # solve simple cases
    record = check_positions(record, groups, verbose)

    unknown, missing = stats(record, groups)
    if verbose:
        print('set: ' + ''.join(record) + f': {missing} missing # in {len(unknown)} gaps')
    if missing == 0:
        return 1

    # split the record into tokens (separated by .)
    record = ''.join(record)
    record = re.sub(r'\.+', '.', record)
    tokens = [token for token in record.split('.') if token]

    Nt = len(tokens)
    Ng = len(groups)
    if debug: 
        print(f'{Nt} tokens: {tokens}')
        print(f'{Ng} groups: {groups}')

    # compile patterns for each set of groups[i:j+1]
    patterns = np.zeros((Ng,Ng), dtype=object)
    for i in range(Ng):
        for j in range(i,Ng):
            patterns[i,j] = match_pattern(groups[i:j+1], flexible = True)     

    cache = -np.ones((Nt,Ng), dtype=int)

    def check_tokens(start_token, start_group, tabs=''):
    # ways to fit groups[start_token:] into tokens[start_group:]

        nonlocal cache

        if debug: print(f'{tabs}Checking groups {start_group}:{Ng} on tokens {start_token}:{Nt}')

        # check if already cached
        if cache[start_token, start_group] >= 0:
            if debug: print(f'{tabs}  cached: {cache[start_token,start_group]}')
            return cache[start_token, start_group]
        else:
            cache[start_token, start_group] = 0

        # # if last token and last group
        # if start_token == Nt-1 and start_group == Ng-1:
        #     return exhaustive(tokens[start_token], [groups[start_group]])
        
        nopts = 0
        for i in range(start_token, Nt): # allows "skipping" tokens
            for j in range(start_group, Ng):

                if debug: print(f'{tabs}  trying groups {start_group}:{j} ({groups[start_group:j+1]}) on token {i} ({tokens[i]})')

                # if there are groups left, but no more tokens
                if i == Nt-1 and j < Ng-1: 
                    if debug: print(f'{tabs}  no tokens left')
                    continue

                # check if groups[start_group:j+1] fit into token i
                if patterns[start_group,j].match(tokens[i]) is None:
                    if debug: print(f'{tabs}  no match')
                    break

                # if there are tokens left, but no more groups
                if j == Ng-1 and i < Nt-1:
                    if any(['#' in t for t in tokens[i+1:]]): 
                        if debug: print(f'{tabs}  no match (extra tokens)')
                        break

                # otherwise check also if groups[start_group+1:] fit into tokens[i+1:]
                if j < Ng-1 and i < Nt-1:
                    if patterns[j+1,Ng-1].match('.'.join(tokens[i+1:])) is None:
                        if debug: print(f'{tabs}  no match on remaining tokens')
                        continue # fitting more groups might solve it

                # ways to fit groups[start_group:j+1] into token i
                n = exhaustive(tokens[i], groups[start_group:j+1])
                if debug: print(f'{tabs}  found {n} ways to fit groups {start_group}:{j} into token {i}')
                
                # ways to fit groups[j+1:] into tokens [i+1:]
                if j == Ng-1 or i == Nt-1:
                    m = 1
                else:
                    m = check_tokens(i+1, j+1, tabs + '  ')

                if debug: print(f'{tabs}  total: {nopts} + {m*n}')
                nopts += n*m

        cache[start_token, start_group] = nopts
        if debug: print(f'{tabs}Cached ({start_token},{start_group}): {nopts}') 
        return nopts
    
    return check_tokens(0,0)

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day12.py [-v] [--part 1]
        python3 -m day12.py --file data.txt [-v] [--part 1]''')
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

    total = 0
    for i, line in enumerate(lines):
        values = parse_line(line, args.part, args.verbose)
        total += values

        progress = (i + 1) / len(lines) * 100
        print(f'Progress: {progress:.2f}%')

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return total
    else:
        print(f'Score: {total}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

