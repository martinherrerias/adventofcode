#! /usr/bin/env python3

'''
Advent of Code 2023 - Day08
'''

from math import comb
import sys
import argparse
import inspect
import re

from collections import namedtuple
import numpy as np

Node = namedtuple('Node', ['id', 'L', 'R'])

def parse_node(line):
    return Node(*re.findall(r'(\w{3})', line))

# def pick(directions, nodes, counter, idx, verbose=False):
            
        
#             next = pick(counter, nodes[idx].left, nodes[idx].right)
#         if args.verbose:
#             print(f'[{counter:03}] {node[idx]} -> {next}')
#         idx = node.index(next)
#         counter += 1

def parse_args():
    parser = argparse.ArgumentParser(usage= '''Usage:
        cat data.txt | day08.py [-v] [--part 1]
        python3 -m day08.py --file data.txt [-v] [--part 1]''')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--part', type=int, default=2, help='Specify the part number')
    parser.add_argument('--file', type=str, help='Specify input file')
    parser.add_argument('--test', action='store_true', help='Test mode')

    args = parser.parse_args()
    if args.debug:
        args.verbose = True
    return args

def main(args):

    if args.file:
        with open(args.file) as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    directions = lines[0].strip()
    n_steps = len(directions)
    
    nodes = [parse_node(line) for line in lines[1:] if line.strip()]
    n_nodes = len(nodes)

    # Convert node ids to indices
    ids = [x.id for x in nodes]
    nodes = [Node(ids.index(n.id), ids.index(n.L),ids.index(n.R)) for n in nodes]

    if args.verbose:
        print(f'Read {len(nodes)} nodes, {n_steps} directions')

    if args.part == 1:
        starting_nodes = np.array([ids.index('AAA')])
        is_end_node = np.array([id == 'ZZZ' for id in ids])
    else:
        starting_nodes = np.array([i for i, x in enumerate(ids) if x[-1] == 'A'])
        is_end_node = np.array([id[-1] == 'Z' for id in ids])

    if args.verbose:
        print(f'Starting nodes: {starting_nodes}, end nodes: {np.nonzero(is_end_node)[0]}')

    # Memoize the result of running all directions starting from each node
    node_table = np.zeros((n_nodes, n_steps), dtype=int)
    end_node_table = np.zeros((n_nodes, n_steps), dtype=bool)

    idx = range(n_nodes)
    for j, d in enumerate(directions):
        next = [nodes[i][(d == 'R') + 1] for i in idx]
        node_table[:,j] = next
        end_node_table[:,j] = is_end_node[next]
        idx = next

    if args.debug:
        print(f'node_table: {node_table}')
        print(f'end_node_table: {end_node_table}')

    # Shorten the tables by removing steps that don't have end nodes
    have_end_node = np.any(end_node_table, axis = 0)

    of = np.nonzero(have_end_node)[0] # step indices with end nodes
    nt = node_table[:, have_end_node]
    et = end_node_table[:, have_end_node]

    if args.debug:
        print(f'nt: {nt}')
        print(f'et: {et}')
        print(f'of: {of}')

    if args.verbose:
        print(f'{sum(have_end_node)} steps have end nodes: {of}')

    # repeat the same steps n_reps times
    # (allow loop to run using larger chunks of steps)

    node_table = []
    end_node_table = []
    offsets = []

    # We want everything to fit in ~ 2**24 L3 cache
    n_reps = 2**24 // sum(map(sys.getsizeof,(nt, et, of)))

    # In the worst case, the number of "states" is choose(nodes, starts)
    n_reps = min(n_reps, comb(n_nodes, len(starting_nodes)) // n_steps)

    if args.verbose:
        print(f'Running {n_reps} repetitions')

    next = range(n_nodes)
    for j in range(n_reps):
        node_table.append(nt[next,:])
        end_node_table.append(et[next,:])
        offsets.append(of + n_steps*j)
        next = nt[next, -1]

    n_steps = n_steps * n_reps

    node_table = np.concatenate(node_table, axis = 1)
    end_node_table = np.concatenate(end_node_table, axis = 1)
    offsets = np.concatenate(offsets)

    if args.debug:
        print(f'offsets: {offsets}')
        print(f'node_table: {node_table}')
        print(f'end_node_table: {end_node_table}')

    if args.test:
        been_there = set()

    counter = 0
    idx = starting_nodes
    while True:
        if args.test:
            h = hash(tuple(idx))
            assert (not h in been_there), f'Full circle after {counter} steps'
            been_there.add(h)

        if args.debug:
            print(f'node_table[idx, :]: {node_table[idx, :]}')

        end_condition = np.all(end_node_table[idx, :], axis = 0)

        if any(end_condition):
            counter += np.min(offsets[end_condition]) + 1
            if args.verbose:
                print(f'counter: {counter}, idx: {idx}, offsets: {offsets[end_condition]}')
            break
        else:
            counter += n_steps
            idx = node_table[idx, -1]

            if args.verbose and np.log2(counter/n_steps) % 1 == 0:
                if args.test:
                    print(f'{counter}: {idx} tried {len(been_there)} starts')
                else:
                    print(f'{counter}: {idx}')

    frame = inspect.currentframe().f_back
    if frame.f_code.co_nlocals > 0:
        return counter
    else:
        print(f'Steps: {counter}')

if __name__ == '__main__':
    args = parse_args()
    main(args)

