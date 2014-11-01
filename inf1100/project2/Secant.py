#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

from math import sin

class RootNotFoundException(Exception):
    pass

# x1 is x[n - 1]
# x2 is x[n - 2]
def iterate(f, x, x1, x2):
    fx1 = f(x1)
    fx2 = f(x2)
    if fx1 - fx2 == 0.0:
        raise RootNotFoundException("division by zero in secant method: %.2f %.2f %.2f" % (x, x1, x2))
    newx = x1 - fx1*(x1 - x2) / (fx1 - fx2)
    return [newx, x, x1]

def secant(f, x, x1, x2, epsilon=1.0E-7, N=100):
    x = float(x)
    x1 = float(x1)
    x2 = float(x2)
    n = 0
    while abs(f(x)) > epsilon and n <= N:
        [x, x1, x2] = iterate(f, x, x1, x2)
        n += 1
    return [x, n]

def main():
    f = lambda x: x**5 - sin(x)

    x = 0.0
    x1 = 0.0
    x2 = 0.0
    print "trying to find zero near 0.0"
    print secant(f, x, x1, x2)

    x = 1.0
    x1 = 0.9
    x2 = 0.8
    print "trying to find zero near 1.0"
    print secant(f, x, x1, x2)

    x = -1.0
    x1 = -0.9
    x2 = -0.8
    print "trying to find zero near -1.0"
    print secant(f, x, x1, x2)

    'entry point'

if __name__ == '__main__':
    main()

