#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

PRECISION = 7
from math import sin

class RootNotFoundException(Exception):
    pass

def iterate(f, x1, x2):
    # x1 is x[n - 1]
    # x2 is x[n - 2]
    fx1 = f(x1)
    fx2 = f(x2)
    if fx1 - fx2 == 0.0:
        raise RootNotFoundException("division by zero in secant method: %.2f %.2f %.2f" % (x, x1, x2))
    x = x1 - fx1*(x1 - x2) / (fx1 - fx2)
    return [x, x1]

def secant(f, x1, x2, dfdx=None, epsilon=1.0E-7, N=100):
    'dfdx is include for compatible method signature'
    x = float(x1)
    x1 = float(x2)
    n = 0
    while abs(f(x)) > epsilon and n <= N:
        status = ('secant: ~[x: %s, x1: %s, n: %d]' %
                    (formatFloat(x), formatFloat(x1), n))
        yield [status, [x, x1, n]]
        [x, x1] = iterate(f, x, x1)
        n += 1
    status = ('found secant: ~[x: %s, x1: %s, n: %d]' %
                (formatFloat(x), formatFloat(x1), n))
    yield [status, [x, x1, n]]

def formatFloat(x):
    return ('%.' + str(PRECISION) + 'f') % x

def test_root_finder(root_finder):
    f = lambda x: x**5 - sin(x)

    x1 = -0.1
    x2 = 0.1
    print "trying to find zero near 0.0"
    [x, n] =  root_finder(f, x1, x2)
    print '~%s after %d iterations' % (formatFloat(x), n)

    x1 = 1.1
    x2 = 0.9
    print "trying to find zero near 1.0"
    [x, n] =  root_finder(f, x1, x2)

def formatFloat(x):
    return ('%.' + str(PRECISION) + 'f') % x


def test_root_finder_1(root_finder, x1, x2):
    f = lambda x: x**5 - sin(x)
    print "trying to find zero in [%.2f, %.2f]" % (x1, x2)
    for status, _ in root_finder(f, x1, x2):
        print status

def test_root_finder(root_finder):
    test_root_finder_1(root_finder, -0.1, 0.1)
    test_root_finder_1(root_finder, -0.9, 1.1)
    test_root_finder_1(root_finder, -0.9, -1.1)

def main():
    'entry point'
    test_root_finder(secant)

if __name__ == '__main__':
    main()

# Run example
'''
trying to find zero near 0.0
~0.0000000 after 1 iterations
trying to find zero near 1.0
~0.9610369 after 5 iterations
trying to find zero near -1.0
~-0.9610369 after 5 iterations
'''
