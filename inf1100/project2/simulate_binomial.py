#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import random
from math import factorial

def binomial(p, n, x):
    return factorial(n) * p**x * (1 - p)**(n - x) / (factorial(x) * factorial(n - x))

def simulate_binomial(p, n, x):
    N = 100000
    M = 0
    for _ in range(N):
        pcount = 0
        rnd = random.Random()
        for i in range(n):
            if rnd.uniform(0, 1) <= p:
                pcount += 1
        if pcount == x:
            M += 1
    sim = float(M) / N
    exact = binomial(p, n, x)
    return [sim, exact]

def test():
    # 4.23 b)
    p, n, x = (0.5, 5, 2)
    [sim, exact] = simulate_binomial(p, n, x)
    print 'coin sim/exact: %.7f %.7f' % (sim, exact)

    # 4.23 c)
    p, n, x = (1/6.0, 4, 4)
    [sim, exact] = simulate_binomial(p, n, x)
    print 'dice sim/exact: %.7f %.7f' % (sim, exact)

    # 4.23 d)
    p, n, x = (1/120.0, 5, 0)
    print 'skiers sim/exact: %.7f %.7f' % (sim, exact)

def main():
    'entry point'
    test()

if __name__ == '__main__':
    main()

# Run example:
'''

coin sim/exact: 0.3129400 0.3125000
dice sim/exact: 0.0007000 0.0007716
skiers sim/exact: 0.0007000 0.0007716
'''
