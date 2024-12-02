#! /usr/bin/env python3

import numpy as np
import re

from day12 import *

line = '.??..??...?##. 1,1,3'
verbose = True

groups = list(map(int, re.findall(r'(\d+)', line)))
record = re.match(r'^[?.#]+', line).group(0)

groups = groups*5
record = '?'.join([record]*5)

if verbose:
    unknown, missing = stats(record, groups)
    print(f'\nraw: ' + ''.join(record) + f': {missing} missing # in {len(unknown)} gaps')

# solve simple cases
record = check_positions(record, groups, verbose)

unknown, missing = stats(record, groups)
if verbose:
    print('set: ' + ''.join(record) + f': {missing} missing # in {len(unknown)} gaps')
# if missing == 0:
#     return 1

# split the record into tokens (separated by .)
record = ''.join(record)
record = re.sub(r'\.+', '.', record)
tokens = record.split('.')

Nt = len(tokens)
Ng = len(groups)

patterns = np.zeros((Ng,Ng), dtype=object)
for i in range(Ng):
    for j in range(Ng):
        patterns[i,j] = match_pattern(groups[i:j+1], flexible = True)

cache = -np.ones((Nt,Ng), dtype=int)

def check_tokens(start_token, start_group):
# ways to fit groups[start_token:] into tokens[start_group:]

    # check if already cached
    if cache[start_token,start_group] >= 0:
        return cache[start_token,start_group]

    # if last token and last group
    if start_token == Nt-1 and start_group == Ng-1:
        return exhaustive(tokens[start_token], groups[start_group])
    
    nopts = 0
    for i in range(start_token, Nt):
        for j in range(start_group, Ng):

            # check if groups[start_group:j+1] fit into token i
            groups_fit = patterns[start_group,j].match(tokens[i]) is not None

            # if there are groups left, but no more tokens
            if i == Nt-1 and j < Ng-1: break
            
            # if there are tokens left, but no more groups
            if j == Ng-1 and i < Nt-1:
                if any(['#' in t for t in tokens[i+1:]]): break

            # otherwise check also if groups[start_group+1:] fit into tokens[i+1:]
            if j < Ng-1 and i < Nt-1:
                groups_fit &= patterns[j+1,Ng].match('.'.join(tokens[i+1:])) is not None

            if groups_fit:
                # ways to fit groups[start_group:j+1] into token i
                n = exhaustive(tokens[i], groups[start_group:j+1])
                
                # ways to fit groups[j+1:] into tokens [i+1:]
                if j == Ng-1 and i < Nt-1:
                    m = 1
                else:
                    m = check_tokens(i+1, j+1)

                nopts += n*m
    return nopts