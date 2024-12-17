#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
from collections import defaultdict

MAX_BITS = 128

class BitRange():

    def __init__(self, lo = None, hi = None):
        self.lo = lo
        self.hi = hi

    @property
    def n(self):
        return self.hi - self.lo

    def update(self, n):
        self.lo = min(self.lo, n) if self.lo is not None else n
        self.hi = max(self.hi, n+1) if self.hi is not None else n+1

    def set(self, number, value):
        """
        Set bits of number in the range [lo, hi) to value
        """

        assert value >> self.n == 0

        mask = (1 << self.n) - 1
        number &= ~(mask << self.lo)
        number |= value << self.lo

        return number
    
    def __repr__(self):
        return f'BitRange({self.lo}, {self.hi})'


class Computer():

    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.ptr = 0
        self._out = []

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

    def run(self, a = None):

        if a is not None:
            self.a = a
        
        self._out = []
        self.ptr = 0
        while self.ptr < len(self.program):
            ins = self.program[self.ptr]
            op = self.program[self.ptr + 1]
            self.instructions()[ins](self, op)

        return self._out

    def quine(self):
        """
        Find a value of A that causes the program to print itself
        """

        influence = defaultdict(BitRange)

        # Get the range of bits that influence each printed output
        # influence[j] = BitRange(i,k) means bits [i, k) of A set output[j]
        for n in range(MAX_BITS):
            min_len = len(self.run(2**n))
            max_len = len(self.run(2**(n+1)-1))
            assert min_len == max_len

            if min_len > len(self.program):
                break

            influence[min_len-1].update(n)

        # Recursively find values for the bits in influence[j, j-1, ... 0]
        # that cause the output[j:] to match the program[j:]
        def _find_output(j, a0):

            bit_range = influence[j]

            for x in range(2**bit_range.n):

                a = bit_range.set(a0, x)
                out = self.run(a = a)

                if len(out) == len(self.program) and out[j:] == self.program[j:]:
                    if j == 0:
                        return a
                    else:
                        a = _find_output(j-1, a)
                        if a is not None:
                            return a
                        else:
                            continue

            return None

        return _find_output(len(self.program)-1, 0)


    def combo(self, op):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        else:
            raise ValueError('Unknown combo operand')

    def adv(self, op):
        self.a = self.a // 2 ** self.combo(op)
        self.ptr += 2

    def bxl(self, op):
        self.b = self.b ^ op
        self.ptr += 2

    def bst(self, op):
        self.b = self.combo(op) % 8
        self.ptr += 2

    def jnz(self, op):
        if self.a == 0:
            self.ptr += 2
        else:
            self.ptr = op

    def bxc(self, op):
        self.b = self.b ^ self.c
        self.ptr += 2

    def out(self, op):
        self._out.append(self.combo(op) % 8)
        self.ptr += 2

    def bdv(self, op):
        self.b = self.a // 2 ** self.combo(op)
        self.ptr += 2

    def cdv(self, op):
        self.c = self.a // 2 ** self.combo(op)
        self.ptr += 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    return parser.parse_args()

def main(file=None, part=None):

    cmp = Computer.from_file(file)

    if part == 1:
        return ','.join([str(x) for x in cmp.run()])
    elif part == 2:
        return cmp.quine()
    else:
        raise ValueError(f'Invalid part number: {part}')

if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part)
        print(f'Part {part}: {total}')
