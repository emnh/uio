#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

from math import sin, cos
from Secant import secant, PRECISION, formatFloat

def newton(f, x1, x2, dfdx, epsilon=1.0E-7, N=100):
    # use midpoint of interval as x1
    x = (float(x1) + float(x2)) / 2.0
    n = 0
    while abs(f(x)) > epsilon and n <= N:
        status = ('newton: ~[x: %s, n: %d]' %
                    (formatFloat(x), n))
        yield [status, [x, n]]

        x = x - f(x) / dfdx(x)
        n += 1
    status = ('found newton: ~[x: %s, n: %d]' %
                (formatFloat(x), n))
    yield [status, [x, n]]

def bisection(f, x1, x2, dfdx=None, epsilon=1.0E-7, N=100):
    'dfdx is included for compatible method signature'
    a = float(x1)
    b = float(x2)
    n = 0
    fa = f(a)
    while abs(a - b) > epsilon and n <= N:
        status = ('bisection: ~[a: %s, b: %s, n: %d]' %
                    (formatFloat(a), formatFloat(b), n))
        yield [status, [a, b, n]]

        m = (a + b) / 2.0
        fm = f(m)
        if fa*fm <= 0:
            b = m
        else:
            a = m
            fa = fm
        n += 1
    status = ('found bisection: ~[a: %s, b: %s, n: %d]' %
                (formatFloat(a), formatFloat(b), n))
    yield [status, [a, b, n]]

class RootTest(object):

    def __init__(self, f, dfdx, root_intervals):
        self.f = f
        self.dfdx = dfdx
        self.root_intervals = root_intervals

def main():
    'entry point'
    root_tests = [
        RootTest(
            f=lambda x: x**5 - sin(x),
            dfdx=lambda x: 5*x**4 - cos(x),
            root_intervals=[[-0.1, 1.0], [0.9, 1.1], [-1.1, -0.9]]
            )
        ]

    root_finders = [secant, bisection, newton]
    for root_test in root_tests:
        f = root_test.f
        dfdx = root_test.dfdx
        for a, b in root_test.root_intervals:
            for root_finder in root_finders:
                for status, _ in root_finder(f, a, b, dfdx):
                    laststatus = status
                    #print status
                print laststatus

if __name__ == '__main__':
    main()
