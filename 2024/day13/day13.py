#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
import re
from collections import namedtuple

import numpy as np
from scipy.optimize import LinearConstraint, Bounds, milp

Problem = namedtuple('Problem', ['a', 'b', 'p'])
Cost = namedtuple('Cost',['a','b'])

COST = Cost(a=3, b=1)

def solve_problem(problem, upper = 100):

    DTYPE = np.uint64
    c = np.array(COST, dtype=DTYPE)

    A = np.array([problem.a, problem.b], dtype=DTYPE).transpose()
    
    # In principle we should solve p <= Ax <= p, but this fails for part 2
    # adding some slack for floating point errors seems to work, no idea why
    lb = np.array(problem.p, dtype=DTYPE) - 0.5
    ub = np.array(problem.p, dtype=DTYPE) + 0.5

    res = milp(c=np.array(COST, dtype=DTYPE),
               bounds = Bounds(0,upper),
               constraints=LinearConstraint(A, lb, ub),
               integrality=np.ones_like(c)*3)

    if res.success:
        return int(res.fun)
    elif res.status ==2:
        return None
    else:
        raise ValueError('Unexpected result\n{problem}\n{res}')
    
def part_1(problem):
    return solve_problem(problem, upper = 100)

def part_2(problem):
    prize = tuple(x + 10000000000000 for x in problem.p)
    tweaked = Problem(problem.a, problem.b, prize)
    return solve_problem(tweaked, upper = np.inf)


def parse_input(text):

    match = re.match(r'Button A: X\+(\d+), Y\+(\d+)\n'
                     r'Button B: X\+(\d+), Y\+(\d+)\n'
                     r'Prize: X=(\d+), Y=(\d+)', text)
    if not match:
        raise ValueError(f"Bad input:\n{text}")
    
    a_x, a_y, b_x, b_y, p_x, p_y = map(int, match.groups())
    return Problem((a_x, a_y), (b_x, b_y), (p_x, p_y))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def main(file=None, part=None, verbose=False):

    with open(file, encoding='utf-8') as f:
        text = f.read()

    problems = [parse_input(chunk) for chunk in text.split('\n\n')]

    if part == 1:
        values = [part_1(p) for p in problems]
    elif part == 2:
        values = [part_2(p) for p in problems]
    else:
        raise ValueError(f'Invalid part number: {part}')

    total = sum(v for v in values if v is not None)
    
    if verbose:
        for i, value in enumerate(values):
            print(f'{problems[i]}: {value}')

    return total


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
