#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import random

def game(strategy):
    [p, q] = [1, 100]
    secret = random.randint(p, q)
    attempts = 0
    guess = 0
    while guess != secret:
        guess = strategy(p, q)
        attempts += 1
        if guess < secret:
            p = guess + 1
        elif guess > secret:
            q = guess - 1
    return attempts

def main():
    'entry point'
    binary_search = lambda p, q: (p + q) / 2
    blind_fold = lambda p, q: random.randint(p, q)
    N = 10000
    bin_avg = 0.0
    blind_avg = 0.0
    for i in range(N):
        bin_avg += game(binary_search)
        blind_avg += game(blind_fold)
    bin_avg /= N
    blind_avg /= N
    print 'bin', bin_avg
    print 'blind', blind_avg


if __name__ == '__main__':
    main()

# Clearly, binary search is superior.
# Run example:
'''
bin 5.7886
blind 7.4743
'''
