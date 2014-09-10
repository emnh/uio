#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import os
import sys
import re
from math import pi, sin

# a)
def S(t, n, T):
    fy = lambda i: sin(2 * (2 * i - 1) * pi * t / T) / (2*i - 1)
    s = 4.0 / pi * sum(fy(x) for x in range(1, n + 1))
    return s

# b)
def f(t, T):
    if 0 < t < T / 2.0:
        ret = 1
    elif t == T / 2.0:
        ret = 0
    elif T / 2.0 < t < T:
        ret = -1
    return ret

def compute_error():
    T = 2 * pi
    for a in [0.01, 0.25, 0.49]:
        for n in [1,3,5,10,30,100]:
            t = a * T
            s = S(t, n, T)
            y = f(t, T)
            print 'n', n, 'alpha', a, 'S(t, n, T) - f(t, T)', s - y

def main():
    'entry point'
    compute_error()

if __name__ == '__main__':
    main()

# Run example
# c)
# The approximation is more accurate for higher n.
# The approximation converges faster when alpha = 0.25.
'''
n 1 alpha 0.01 S(t, n, T) - f(t, T) -0.920052627501
n 3 alpha 0.01 S(t, n, T) - f(t, T) -0.761834996162
n 5 alpha 0.01 S(t, n, T) - f(t, T) -0.608585435311
n 10 alpha 0.01 S(t, n, T) - f(t, T) -0.266797434877
n 30 alpha 0.01 S(t, n, T) - f(t, T) 0.14481610778
n 100 alpha 0.01 S(t, n, T) - f(t, T) -0.050094008341
n 1 alpha 0.25 S(t, n, T) - f(t, T) 0.273239544735
n 3 alpha 0.25 S(t, n, T) - f(t, T) 0.103474272104
n 5 alpha 0.25 S(t, n, T) - f(t, T) 0.0630539690963
n 10 alpha 0.25 S(t, n, T) - f(t, T) -0.0317523771092
n 30 alpha 0.25 S(t, n, T) - f(t, T) -0.0106073863054
n 100 alpha 0.25 S(t, n, T) - f(t, T) -0.00318301929431
n 1 alpha 0.49 S(t, n, T) - f(t, T) -0.920052627501
n 3 alpha 0.49 S(t, n, T) - f(t, T) -0.761834996162
n 5 alpha 0.49 S(t, n, T) - f(t, T) -0.608585435311
n 10 alpha 0.49 S(t, n, T) - f(t, T) -0.266797434877
n 30 alpha 0.49 S(t, n, T) - f(t, T) 0.14481610778
n 100 alpha 0.49 S(t, n, T) - f(t, T) -0.050094008341
'''
