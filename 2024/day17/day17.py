#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path

class Computer():

    def __init__(self, a, b, c, program):
        self.reg_a = a
        self.reg_b = b
        self.reg_c = c
        self.program = program
        self.pointer = 0
        self.out = []

    @classmethod
    def from_file(cls, file):

        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        a = int(lines[0].removeprefix('Register A: '))
        b = int(lines[1].removeprefix('Register B: '))
        c = int(lines[2].removeprefix('Register C: '))
        program = [int(x) for x in lines[4].removeprefix('Program: ').split(',')]

        return cls(a, b, c, program)

    @classmethod
    def instructions(cls):
        return {
            0: cls.adv,
            1: cls.bxl,
            2: cls.bst,
            3: cls.jnz,
            4: cls.bxc,
            5: cls.out,
            6: cls.bdv,
            7: cls.cdv
        }

    def run(self, verbose = False):
        while self.pointer < len(self.program):
            ins = self.program[self.pointer]
            op = self.program[self.pointer + 1]
            self.instructions()[ins](self, op)

    def combo(self, op):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return self.reg_a
        elif op == 5:
            return self.reg_b
        elif op == 6:
            return self.reg_c
        else:
            raise ValueError('Unknown combo operand')

    def adv(self, op):
        self.reg_a = self.reg_a // 2 ** self.combo(op)
        self.pointer += 2

    def bxl(self, op):
        self.reg_b = self.reg_b ^ op
        self.pointer += 2

    def bst(self, op):
        self.reg_b = self.combo(op) % 8
        self.pointer += 2

    def jnz(self, op):
        if self.reg_a == 0:
            self.pointer += 2
        else:
            self.pointer = op

    def bxc(self, op):
        self.reg_b = self.reg_b ^ self.reg_c
        self.pointer += 2

    def out(self, op):
        self.out.append(self.combo(op) % 8)
        self.pointer += 2

    def bdv(self, op):
        self.reg_b = self.reg_a // 2 ** self.combo(op)
        self.pointer += 2

    def cdv(self, op):
        self.reg_c = self.reg_a // 2 ** self.combo(op)
        self.pointer += 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def main(file=None, part=None, verbose=False):

    cmp = Computer.from_file(file)
    cmp.run(verbose=verbose)

    if part == 1:
        return ','.join([str(x) for x in cmp.out])
    elif part == 2:
        return None
    else:
        raise ValueError(f'Invalid part number: {part}')

if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
