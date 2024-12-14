#! /usr/bin/env python3
'''
Advent of Code 2024 - https://adventofcode.com/2024/
'''

import argparse
from pathlib import Path
import re
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

import numpy as np

from scipy.ndimage import gaussian_filter


def pair(xy):
    assert len(xy) == 2, f'bad pair: {xy}'
    return np.array(xy, dtype=int)

def blur(img, sigma):
    # Turns out not to be necessary, but it does yield a clearer signal

    blurred = img.astype('float')
    blurred = gaussian_filter(blurred, sigma=sigma)
    blurred = (blurred / np.max(blurred)) * 255
    return blurred.astype('uint8')

def entropy(img, sigma=0):
    # https://stackoverflow.com/a/55067289/22293982

    blurred = blur(img, sigma)
    marg = np.histogramdd(np.ravel(blurred), bins = 256)[0]/img.size
    marg = list(filter(lambda p: p > 0, np.ravel(marg)))
    return -np.sum(np.multiply(marg, np.log2(marg)))

class Robot:
    def __init__(self, p, v):
        self.p = pair(p)
        self.v = pair(v)

    @classmethod
    def from_string(cls, s):
        m = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', s)
        if not m:
            raise ValueError(f'Failed to parse robot from: {s}')
        g = [int(g) for g in m.groups()]
        return Robot(g[0:2], g[2:4])

class Room:
    def __init__(self, file):

        with open(file, encoding='utf-8') as f:
            lines = f.readlines()

        size = [int(g) for g in re.match(r'# room=(\d+),(\d+)', lines[0]).groups()]
        self.size = pair(size)
        assert all(s % 2 == 1 for s in size)

        robots = [Robot.from_string(s) for s in lines[1:]]
        self.p = np.vstack([r.p for r in robots])
        self.v = np.vstack([r.v for r in robots])
        self._p0 = self.p.copy

        assert np.all((self.p[:,0] >= 0) & (self.p[:,0] <= self.size[0]))
        assert np.all((self.p[:,1] >= 0) & (self.p[:,1] <= self.size[1])) 
    
    @property
    def robots(self):
        return [Robot(p,v) for p,v in zip(self.p, self.v)]
    
    def move(self, steps):
        return (self.p + steps*self.v) % self.size

    def reset(self):
        self.p[:] = self._p0[:]

    def quadrant_counts(self, t=0):

        p = self.move(t)
        counts = [0,0,0,0]
        for n in range(4):
            if n < 2:
                q = p[:,0] < self.size[0] // 2
            else:
                q = p[:,0] > self.size[0] // 2
            if n % 2 == 0:
                q[q] = p[q,1] < self.size[1] // 2
            else:
                q[q] = p[q,1] > self.size[1] // 2
            counts[n] = sum(q)
        return counts

    def safety_factor(self, t=0):
        return np.prod(self.quadrant_counts(t))

    def image(self, t=0):
        p, counts = np.unique(self.move(t), axis=0, return_counts=True)
        img = np.zeros(np.flip(self.size), dtype=int)
        img[p[:,1],p[:,0]] = counts
        return img

    def frame(self, t=0, sigma = 0):

        img = self.image(t)
        if sigma:
            img = blur(img, sigma)

        fig = plt.figure(2)
        plt.title(f't = {t}')
        im = plt.imshow(img)
        plt.show(block=False)

    def entropy_plot(self, steps, sigma = 2):

        plt.figure(3)
        e = [entropy(blur(self.image(t), sigma)) for t in range(steps)]
        plt.plot(range(steps), e)
        plt.show(block=False)

    def entropy_search(self, sigma=2, steps=10000):

        fig = plt.figure(1)
        im = plt.imshow(self.image(0))
        plt.show(block=False)

        best_e = np.inf
        best_t = 0
        for t in range(steps):

            img = self.image(t)
            e = entropy(blur(img, sigma))

            if e < best_e:
                best_e = e
                best_t = t
                plt.title(f't = {t}, entropy = {e:,.3f}')
                im.set_array(self.image(t))
                fig.canvas.draw_idle()
                fig.canvas.flush_events()

        return best_t


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default=Path(__file__).with_suffix('.dat'), 
        help='Input file, default: %(default)s')
    parser.add_argument('--part', type=int, nargs='+', default=[1, 2],
        help='Part number(s), default: %(default)s')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def main(file=None, part=None, verbose=False):

    room = Room(file)

    if part == 1:
        return room.safety_factor(100)
    elif part == 2:
        return room.entropy_search()
    else:
        raise ValueError(f'Invalid part number: {part}')


if __name__ == '__main__':

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f'Part {part} total: {total}')
