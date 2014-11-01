#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

from math import sin, cos, pi, tanh, cosh
from Secant import secant, PRECISION, formatFloat
import sys

def sech(x):
    return 2*cosh(x) / (cosh(2*x) + 1)

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
    status = ('newton: ~[x: %s, n: %d]' %
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
    status = ('bisection: ~[a: %s, b: %s, n: %d]' %
                (formatFloat(a), formatFloat(b), n))
    yield [status, [a, b, n]]

class RootTest(object):

    def __init__(self, f, fp, dfdx, root_intervals):
        self.f = f
        self.fp = fp
        self.dfdx = dfdx
        self.root_intervals = root_intervals

def test_roots(root_tests=None):
    dx = 0.1
    if root_tests == None:
        root_tests = [
            RootTest(
                f=lambda x: sin(x),
                fp='sin(x)',
                dfdx=lambda x: cos(x),
                # will find one root on each side of 0, has infinite roots
                root_intervals=[[-dx, dx], [pi-dx, pi+dx], [-pi-dx, -pi+dx]]
                ),
            RootTest(
                f=lambda x: x - sin(x),
                fp='x - sin(x)',
                dfdx=lambda x: 1 - cos(x),
                root_intervals=[[-0.1, 0.1]]
                ),
            RootTest(
                f=lambda x: x**5 - sin(x),
                fp='x^5 - sin(x)',
                dfdx=lambda x: 5*x**4 - cos(x),
                root_intervals=[[-dx, dx], [0.9, 1.1], [-1.1, -0.9]]
                ),
            RootTest(
                f=lambda x: x**4 * sin(x),
                fp='x^4 * sin(x)',
                dfdx=lambda x: x**3*(4*sin(x) + x*cos(x)),
                # will find one root on each side of 0, has infinite roots
                root_intervals=[[-dx, dx], [pi-dx, pi+dx], [-pi-dx, -pi+dx]]
                ),
            RootTest(
                f=lambda x: x**4 - 16,
                fp='x^4 - 16',
                dfdx=lambda x: 4*x**3,
                root_intervals=[[0.0, 5.0], [-5.0, 0]]
                ),
            RootTest(
                f=lambda x: x**10 - 1,
                fp='x^10 - 1',
                dfdx=lambda x: 10*x**9,
                root_intervals=[[0.9, 2.0], [-0.9, -2.0]]
                ),
            RootTest(
                f=lambda x: tanh(x) - 0,
                fp='tanh(x) - 1',
                dfdx=lambda x: sech(x)**2,
                root_intervals=[[-dx, dx]]
                ),
            RootTest(
                f=lambda x: tanh(x) - x**10,
                fp='tanh(x) - x^10',
                dfdx=lambda x: sech(x)**2 - 10*x**9,
                root_intervals=[[-dx, dx], [0.9, 1.1]]
                ),

            ]

    root_finders = [secant, bisection, newton]
    for root_test in root_tests:
        f = root_test.f
        fp = root_test.fp
        dfdx = root_test.dfdx
        for a, b in root_test.root_intervals:
            print 'finding root of %s in [%s, %s]' % (fp, formatFloat(a), formatFloat(b))
            for root_finder in root_finders:
                for status, _ in root_finder(f, a, b, dfdx):
                    laststatus = status
                    print status
                print #laststatus
            #print

def main():
    'entry point'
    if sys.argv[1] == 'test':
        test_roots()
        sys.exit(0)
    if len(sys.argv) < 7:
        print 'usage: %s f dfdx a b x0 x1' % (sys.argv[0])
        sys.exit(-1)
    f = eval('lambda x:' + sys.argv[1])
    fp = sys.argv[1]
    dfdx = eval('lambda x:' + sys.argv[2])
    a = float(sys.argv[3])
    b = float(sys.argv[4])
    x0 = float(sys.argv[5])
    x1 = float(sys.argv[6])
    print 'finding root of %s in [%s, %s]' % (fp, formatFloat(a), formatFloat(b))
    for status, _ in secant(f, x0, x1, dfdx):
        print status
    for status, _ in bisection(f, a, b, dfdx):
        print status
    for status, _ in newton(f, x0, x0, dfdx):
        print status

if __name__ == '__main__':
    main()

# Run example: 
# ./root_finder_examples.py 'sin(x)' 'cos(x)' -0.1 0.1 -0.1 0.1                                                                                           :(
'''
finding root of sin(x) in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]
bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]
newton: ~[x: -0.1000000, n: 0]
newton: ~[x: 0.0003347, n: 1]
newton: ~[x: -0.0000000, n: 2]
'''

# ./root_finder_examples.py test
'''
finding root of sin(x) in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]

bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]

newton: ~[x: 0.0000000, n: 0]

finding root of sin(x) in [3.0415927, 3.2415927]
secant: ~[x: 3.0415927, x1: 3.2415927, n: 0]
secant: ~[x: 3.1415927, x1: 3.0415927, n: 1]

bisection: ~[a: 3.0415927, b: 3.2415927, n: 0]
bisection: ~[a: 3.1415927, b: 3.2415927, n: 1]
bisection: ~[a: 3.1415927, b: 3.1915927, n: 2]
bisection: ~[a: 3.1415927, b: 3.1665927, n: 3]
bisection: ~[a: 3.1415927, b: 3.1540927, n: 4]
bisection: ~[a: 3.1415927, b: 3.1478427, n: 5]
bisection: ~[a: 3.1415927, b: 3.1447177, n: 6]
bisection: ~[a: 3.1415927, b: 3.1431552, n: 7]
bisection: ~[a: 3.1415927, b: 3.1423739, n: 8]
bisection: ~[a: 3.1415927, b: 3.1419833, n: 9]
bisection: ~[a: 3.1415927, b: 3.1417880, n: 10]
bisection: ~[a: 3.1415927, b: 3.1416903, n: 11]
bisection: ~[a: 3.1415927, b: 3.1416415, n: 12]
bisection: ~[a: 3.1415927, b: 3.1416171, n: 13]
bisection: ~[a: 3.1415927, b: 3.1416049, n: 14]
bisection: ~[a: 3.1415927, b: 3.1415988, n: 15]
bisection: ~[a: 3.1415927, b: 3.1415957, n: 16]
bisection: ~[a: 3.1415927, b: 3.1415942, n: 17]
bisection: ~[a: 3.1415927, b: 3.1415934, n: 18]
bisection: ~[a: 3.1415927, b: 3.1415930, n: 19]
bisection: ~[a: 3.1415927, b: 3.1415928, n: 20]
bisection: ~[a: 3.1415927, b: 3.1415927, n: 21]

newton: ~[x: 3.1415927, n: 0]

finding root of sin(x) in [-3.2415927, -3.0415927]
secant: ~[x: -3.2415927, x1: -3.0415927, n: 0]
secant: ~[x: -3.1415927, x1: -3.2415927, n: 1]

bisection: ~[a: -3.2415927, b: -3.0415927, n: 0]
bisection: ~[a: -3.2415927, b: -3.1415927, n: 1]
bisection: ~[a: -3.1915927, b: -3.1415927, n: 2]
bisection: ~[a: -3.1665927, b: -3.1415927, n: 3]
bisection: ~[a: -3.1540927, b: -3.1415927, n: 4]
bisection: ~[a: -3.1478427, b: -3.1415927, n: 5]
bisection: ~[a: -3.1447177, b: -3.1415927, n: 6]
bisection: ~[a: -3.1431552, b: -3.1415927, n: 7]
bisection: ~[a: -3.1423739, b: -3.1415927, n: 8]
bisection: ~[a: -3.1419833, b: -3.1415927, n: 9]
bisection: ~[a: -3.1417880, b: -3.1415927, n: 10]
bisection: ~[a: -3.1416903, b: -3.1415927, n: 11]
bisection: ~[a: -3.1416415, b: -3.1415927, n: 12]
bisection: ~[a: -3.1416171, b: -3.1415927, n: 13]
bisection: ~[a: -3.1416049, b: -3.1415927, n: 14]
bisection: ~[a: -3.1415988, b: -3.1415927, n: 15]
bisection: ~[a: -3.1415957, b: -3.1415927, n: 16]
bisection: ~[a: -3.1415942, b: -3.1415927, n: 17]
bisection: ~[a: -3.1415934, b: -3.1415927, n: 18]
bisection: ~[a: -3.1415930, b: -3.1415927, n: 19]
bisection: ~[a: -3.1415928, b: -3.1415927, n: 20]
bisection: ~[a: -3.1415927, b: -3.1415927, n: 21]

newton: ~[x: -3.1415927, n: 0]

finding root of x - sin(x) in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]

bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]

newton: ~[x: 0.0000000, n: 0]

finding root of x^5 - sin(x) in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]

bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]

newton: ~[x: 0.0000000, n: 0]

finding root of x^5 - sin(x) in [0.9000000, 1.1000000]
secant: ~[x: 0.9000000, x1: 1.1000000, n: 0]
secant: ~[x: 0.9422823, x1: 0.9000000, n: 1]
secant: ~[x: 0.9643069, x1: 0.9422823, n: 2]
secant: ~[x: 0.9608791, x1: 0.9643069, n: 3]
secant: ~[x: 0.9610356, x1: 0.9608791, n: 4]
secant: ~[x: 0.9610369, x1: 0.9610356, n: 5]

bisection: ~[a: 0.9000000, b: 1.1000000, n: 0]
bisection: ~[a: 0.9000000, b: 1.0000000, n: 1]
bisection: ~[a: 0.9500000, b: 1.0000000, n: 2]
bisection: ~[a: 0.9500000, b: 0.9750000, n: 3]
bisection: ~[a: 0.9500000, b: 0.9625000, n: 4]
bisection: ~[a: 0.9562500, b: 0.9625000, n: 5]
bisection: ~[a: 0.9593750, b: 0.9625000, n: 6]
bisection: ~[a: 0.9609375, b: 0.9625000, n: 7]
bisection: ~[a: 0.9609375, b: 0.9617187, n: 8]
bisection: ~[a: 0.9609375, b: 0.9613281, n: 9]
bisection: ~[a: 0.9609375, b: 0.9611328, n: 10]
bisection: ~[a: 0.9610352, b: 0.9611328, n: 11]
bisection: ~[a: 0.9610352, b: 0.9610840, n: 12]
bisection: ~[a: 0.9610352, b: 0.9610596, n: 13]
bisection: ~[a: 0.9610352, b: 0.9610474, n: 14]
bisection: ~[a: 0.9610352, b: 0.9610413, n: 15]
bisection: ~[a: 0.9610352, b: 0.9610382, n: 16]
bisection: ~[a: 0.9610367, b: 0.9610382, n: 17]
bisection: ~[a: 0.9610367, b: 0.9610374, n: 18]
bisection: ~[a: 0.9610367, b: 0.9610371, n: 19]
bisection: ~[a: 0.9610369, b: 0.9610371, n: 20]
bisection: ~[a: 0.9610369, b: 0.9610370, n: 21]

newton: ~[x: 1.0000000, n: 0]
newton: ~[x: 0.9644530, n: 1]
newton: ~[x: 0.9610660, n: 2]
newton: ~[x: 0.9610369, n: 3]

finding root of x^5 - sin(x) in [-1.1000000, -0.9000000]
secant: ~[x: -1.1000000, x1: -0.9000000, n: 0]
secant: ~[x: -0.9422823, x1: -1.1000000, n: 1]
secant: ~[x: -0.9555458, x1: -0.9422823, n: 2]
secant: ~[x: -0.9613057, x1: -0.9555458, n: 3]
secant: ~[x: -0.9610332, x1: -0.9613057, n: 4]
secant: ~[x: -0.9610369, x1: -0.9610332, n: 5]

bisection: ~[a: -1.1000000, b: -0.9000000, n: 0]
bisection: ~[a: -1.0000000, b: -0.9000000, n: 1]
bisection: ~[a: -1.0000000, b: -0.9500000, n: 2]
bisection: ~[a: -0.9750000, b: -0.9500000, n: 3]
bisection: ~[a: -0.9625000, b: -0.9500000, n: 4]
bisection: ~[a: -0.9625000, b: -0.9562500, n: 5]
bisection: ~[a: -0.9625000, b: -0.9593750, n: 6]
bisection: ~[a: -0.9625000, b: -0.9609375, n: 7]
bisection: ~[a: -0.9617187, b: -0.9609375, n: 8]
bisection: ~[a: -0.9613281, b: -0.9609375, n: 9]
bisection: ~[a: -0.9611328, b: -0.9609375, n: 10]
bisection: ~[a: -0.9611328, b: -0.9610352, n: 11]
bisection: ~[a: -0.9610840, b: -0.9610352, n: 12]
bisection: ~[a: -0.9610596, b: -0.9610352, n: 13]
bisection: ~[a: -0.9610474, b: -0.9610352, n: 14]
bisection: ~[a: -0.9610413, b: -0.9610352, n: 15]
bisection: ~[a: -0.9610382, b: -0.9610352, n: 16]
bisection: ~[a: -0.9610382, b: -0.9610367, n: 17]
bisection: ~[a: -0.9610374, b: -0.9610367, n: 18]
bisection: ~[a: -0.9610371, b: -0.9610367, n: 19]
bisection: ~[a: -0.9610371, b: -0.9610369, n: 20]
bisection: ~[a: -0.9610370, b: -0.9610369, n: 21]

newton: ~[x: -1.0000000, n: 0]
newton: ~[x: -0.9644530, n: 1]
newton: ~[x: -0.9610660, n: 2]
newton: ~[x: -0.9610369, n: 3]

finding root of x^4 * sin(x) in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]

bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]

newton: ~[x: 0.0000000, n: 0]

finding root of x^4 * sin(x) in [3.0415927, 3.2415927]
secant: ~[x: 3.0415927, x1: 3.2415927, n: 0]
secant: ~[x: 3.1289244, x1: 3.0415927, n: 1]
secant: ~[x: 3.1433902, x1: 3.1289244, n: 2]
secant: ~[x: 3.1415634, x1: 3.1433902, n: 3]
secant: ~[x: 3.1415926, x1: 3.1415634, n: 4]
secant: ~[x: 3.1415927, x1: 3.1415926, n: 5]

bisection: ~[a: 3.0415927, b: 3.2415927, n: 0]
bisection: ~[a: 3.1415927, b: 3.2415927, n: 1]
bisection: ~[a: 3.1415927, b: 3.1915927, n: 2]
bisection: ~[a: 3.1415927, b: 3.1665927, n: 3]
bisection: ~[a: 3.1415927, b: 3.1540927, n: 4]
bisection: ~[a: 3.1415927, b: 3.1478427, n: 5]
bisection: ~[a: 3.1415927, b: 3.1447177, n: 6]
bisection: ~[a: 3.1415927, b: 3.1431552, n: 7]
bisection: ~[a: 3.1415927, b: 3.1423739, n: 8]
bisection: ~[a: 3.1415927, b: 3.1419833, n: 9]
bisection: ~[a: 3.1415927, b: 3.1417880, n: 10]
bisection: ~[a: 3.1415927, b: 3.1416903, n: 11]
bisection: ~[a: 3.1415927, b: 3.1416415, n: 12]
bisection: ~[a: 3.1415927, b: 3.1416171, n: 13]
bisection: ~[a: 3.1415927, b: 3.1416049, n: 14]
bisection: ~[a: 3.1415927, b: 3.1415988, n: 15]
bisection: ~[a: 3.1415927, b: 3.1415957, n: 16]
bisection: ~[a: 3.1415927, b: 3.1415942, n: 17]
bisection: ~[a: 3.1415927, b: 3.1415934, n: 18]
bisection: ~[a: 3.1415927, b: 3.1415930, n: 19]
bisection: ~[a: 3.1415927, b: 3.1415928, n: 20]
bisection: ~[a: 3.1415927, b: 3.1415927, n: 21]

newton: ~[x: 3.1415927, n: 0]

finding root of x^4 * sin(x) in [-3.2415927, -3.0415927]
secant: ~[x: -3.2415927, x1: -3.0415927, n: 0]
secant: ~[x: -3.1289244, x1: -3.2415927, n: 1]
secant: ~[x: -3.1401032, x1: -3.1289244, n: 2]
secant: ~[x: -3.1416170, x1: -3.1401032, n: 3]
secant: ~[x: -3.1415926, x1: -3.1416170, n: 4]
secant: ~[x: -3.1415927, x1: -3.1415926, n: 5]

bisection: ~[a: -3.2415927, b: -3.0415927, n: 0]
bisection: ~[a: -3.2415927, b: -3.1415927, n: 1]
bisection: ~[a: -3.1915927, b: -3.1415927, n: 2]
bisection: ~[a: -3.1665927, b: -3.1415927, n: 3]
bisection: ~[a: -3.1540927, b: -3.1415927, n: 4]
bisection: ~[a: -3.1478427, b: -3.1415927, n: 5]
bisection: ~[a: -3.1447177, b: -3.1415927, n: 6]
bisection: ~[a: -3.1431552, b: -3.1415927, n: 7]
bisection: ~[a: -3.1423739, b: -3.1415927, n: 8]
bisection: ~[a: -3.1419833, b: -3.1415927, n: 9]
bisection: ~[a: -3.1417880, b: -3.1415927, n: 10]
bisection: ~[a: -3.1416903, b: -3.1415927, n: 11]
bisection: ~[a: -3.1416415, b: -3.1415927, n: 12]
bisection: ~[a: -3.1416171, b: -3.1415927, n: 13]
bisection: ~[a: -3.1416049, b: -3.1415927, n: 14]
bisection: ~[a: -3.1415988, b: -3.1415927, n: 15]
bisection: ~[a: -3.1415957, b: -3.1415927, n: 16]
bisection: ~[a: -3.1415942, b: -3.1415927, n: 17]
bisection: ~[a: -3.1415934, b: -3.1415927, n: 18]
bisection: ~[a: -3.1415930, b: -3.1415927, n: 19]
bisection: ~[a: -3.1415928, b: -3.1415927, n: 20]
bisection: ~[a: -3.1415927, b: -3.1415927, n: 21]

newton: ~[x: -3.1415927, n: 0]

finding root of x^4 - 16 in [0.0000000, 5.0000000]
secant: ~[x: 0.0000000, x1: 5.0000000, n: 0]
secant: ~[x: 0.1280000, x1: 0.0000000, n: 1]
secant: ~[x: 7629.3945312, x1: 0.1280000, n: 2]
secant: ~[x: 0.1280000, x1: 7629.3945312, n: 3]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 4]
secant: ~[x: 1908.9650921, x1: 0.1280000, n: 5]
secant: ~[x: 0.1280000, x1: 1908.9650921, n: 6]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 7]
secant: ~[x: 1907.5301836, x1: 0.1280000, n: 8]
secant: ~[x: 0.1280000, x1: 1907.5301836, n: 9]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 10]
secant: ~[x: 1907.4470565, x1: 0.1280000, n: 11]
secant: ~[x: 0.1280000, x1: 1907.4470565, n: 12]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 13]
secant: ~[x: 1907.3460017, x1: 0.1280000, n: 14]
secant: ~[x: 0.1280000, x1: 1907.3460017, n: 15]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 16]
secant: ~[x: 1907.4739615, x1: 0.1280000, n: 17]
secant: ~[x: 0.1280000, x1: 1907.4739615, n: 18]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 19]
secant: ~[x: 1907.4404792, x1: 0.1280000, n: 20]
secant: ~[x: 0.1280000, x1: 1907.4404792, n: 21]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 22]
secant: ~[x: 1907.3657267, x1: 0.1280000, n: 23]
secant: ~[x: 0.1280000, x1: 1907.3657267, n: 24]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 25]
secant: ~[x: 1907.4147689, x1: 0.1280000, n: 26]
secant: ~[x: 0.1280000, x1: 1907.4147689, n: 27]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 28]
secant: ~[x: 1907.4428357, x1: 0.1280000, n: 29]
secant: ~[x: 0.1280000, x1: 1907.4428357, n: 30]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 31]
secant: ~[x: 1907.5338545, x1: 0.1280000, n: 32]
secant: ~[x: 0.1280000, x1: 1907.5338545, n: 33]
secant: ~[x: 0.1280000, x1: 0.1280000, n: 34]
secant: ~[x: 1907.4360323, x1: 0.1280000, n: 35]
secant: ~[x: 0.1280000, x1: 1907.4360323, n: 36]
secant: ~[x: 0.1280001, x1: 0.1280000, n: 37]
secant: ~[x: 1907.3790681, x1: 0.1280001, n: 38]
secant: ~[x: 0.1280001, x1: 1907.3790681, n: 39]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 40]
secant: ~[x: 1907.5499341, x1: 0.1280001, n: 41]
secant: ~[x: 0.1280001, x1: 1907.5499341, n: 42]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 43]
secant: ~[x: 1907.3878016, x1: 0.1280001, n: 44]
secant: ~[x: 0.1280001, x1: 1907.3878016, n: 45]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 46]
secant: ~[x: 1907.3485503, x1: 0.1280001, n: 47]
secant: ~[x: 0.1280001, x1: 1907.3485503, n: 48]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 49]
secant: ~[x: 1907.4663156, x1: 0.1280001, n: 50]
secant: ~[x: 0.1280001, x1: 1907.4663156, n: 51]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 52]
secant: ~[x: 1907.4634211, x1: 0.1280001, n: 53]
secant: ~[x: 0.1280001, x1: 1907.4634211, n: 54]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 55]
secant: ~[x: 1907.2969072, x1: 0.1280001, n: 56]
secant: ~[x: 0.1280001, x1: 1907.2969072, n: 57]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 58]
secant: ~[x: 1907.4460551, x1: 0.1280001, n: 59]
secant: ~[x: 0.1280001, x1: 1907.4460551, n: 60]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 61]
secant: ~[x: 1907.3489868, x1: 0.1280001, n: 62]
secant: ~[x: 0.1280001, x1: 1907.3489868, n: 63]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 64]
secant: ~[x: 1907.4650068, x1: 0.1280001, n: 65]
secant: ~[x: 0.1280001, x1: 1907.4650068, n: 66]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 67]
secant: ~[x: 1907.2921539, x1: 0.1280001, n: 68]
secant: ~[x: 0.1280001, x1: 1907.2921539, n: 69]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 70]
secant: ~[x: 1907.4603123, x1: 0.1280001, n: 71]
secant: ~[x: 0.1280001, x1: 1907.4603123, n: 72]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 73]
secant: ~[x: 1907.3062301, x1: 0.1280001, n: 74]
secant: ~[x: 0.1280001, x1: 1907.3062301, n: 75]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 76]
secant: ~[x: 1907.4180915, x1: 0.1280001, n: 77]
secant: ~[x: 0.1280001, x1: 1907.4180915, n: 78]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 79]
secant: ~[x: 1907.4328699, x1: 0.1280001, n: 80]
secant: ~[x: 0.1280001, x1: 1907.4328699, n: 81]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 82]
secant: ~[x: 1907.3885517, x1: 0.1280001, n: 83]
secant: ~[x: 0.1280001, x1: 1907.3885517, n: 84]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 85]
secant: ~[x: 1907.3463001, x1: 0.1280001, n: 86]
secant: ~[x: 0.1280001, x1: 1907.3463001, n: 87]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 88]
secant: ~[x: 1907.4730660, x1: 0.1280001, n: 89]
secant: ~[x: 0.1280001, x1: 1907.4730660, n: 90]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 91]
secant: ~[x: 1907.4431661, x1: 0.1280001, n: 92]
secant: ~[x: 0.1280001, x1: 1907.4431661, n: 93]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 94]
secant: ~[x: 1907.5328670, x1: 0.1280001, n: 95]
secant: ~[x: 0.1280001, x1: 1907.5328670, n: 96]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 97]
secant: ~[x: 1907.4389950, x1: 0.1280001, n: 98]
secant: ~[x: 0.1280001, x1: 1907.4389950, n: 99]
secant: ~[x: 0.1280001, x1: 0.1280001, n: 100]
secant: ~[x: 1907.3701815, x1: 0.1280001, n: 101]

bisection: ~[a: 0.0000000, b: 5.0000000, n: 0]
bisection: ~[a: 0.0000000, b: 2.5000000, n: 1]
bisection: ~[a: 1.2500000, b: 2.5000000, n: 2]
bisection: ~[a: 1.8750000, b: 2.5000000, n: 3]
bisection: ~[a: 1.8750000, b: 2.1875000, n: 4]
bisection: ~[a: 1.8750000, b: 2.0312500, n: 5]
bisection: ~[a: 1.9531250, b: 2.0312500, n: 6]
bisection: ~[a: 1.9921875, b: 2.0312500, n: 7]
bisection: ~[a: 1.9921875, b: 2.0117188, n: 8]
bisection: ~[a: 1.9921875, b: 2.0019531, n: 9]
bisection: ~[a: 1.9970703, b: 2.0019531, n: 10]
bisection: ~[a: 1.9995117, b: 2.0019531, n: 11]
bisection: ~[a: 1.9995117, b: 2.0007324, n: 12]
bisection: ~[a: 1.9995117, b: 2.0001221, n: 13]
bisection: ~[a: 1.9998169, b: 2.0001221, n: 14]
bisection: ~[a: 1.9999695, b: 2.0001221, n: 15]
bisection: ~[a: 1.9999695, b: 2.0000458, n: 16]
bisection: ~[a: 1.9999695, b: 2.0000076, n: 17]
bisection: ~[a: 1.9999886, b: 2.0000076, n: 18]
bisection: ~[a: 1.9999981, b: 2.0000076, n: 19]
bisection: ~[a: 1.9999981, b: 2.0000029, n: 20]
bisection: ~[a: 1.9999981, b: 2.0000005, n: 21]
bisection: ~[a: 1.9999993, b: 2.0000005, n: 22]
bisection: ~[a: 1.9999999, b: 2.0000005, n: 23]
bisection: ~[a: 1.9999999, b: 2.0000002, n: 24]
bisection: ~[a: 1.9999999, b: 2.0000000, n: 25]
bisection: ~[a: 2.0000000, b: 2.0000000, n: 26]

newton: ~[x: 2.5000000, n: 0]
newton: ~[x: 2.1310000, n: 1]
newton: ~[x: 2.0115921, n: 2]
newton: ~[x: 2.0000998, n: 3]
newton: ~[x: 2.0000000, n: 4]
newton: ~[x: 2.0000000, n: 5]

finding root of x^4 - 16 in [-5.0000000, 0.0000000]
secant: ~[x: -5.0000000, x1: 0.0000000, n: 0]
secant: ~[x: -0.1280000, x1: -5.0000000, n: 1]
secant: ~[x: -0.2527212, x1: -0.1280000, n: 2]
secant: ~[x: -523.7885957, x1: -0.2527212, n: 3]
secant: ~[x: -0.2527213, x1: -523.7885957, n: 4]
secant: ~[x: -0.2527214, x1: -0.2527213, n: 5]
secant: ~[x: -248.0083238, x1: -0.2527214, n: 6]
secant: ~[x: -0.2527224, x1: -248.0083238, n: 7]
secant: ~[x: -0.2527235, x1: -0.2527224, n: 8]
secant: ~[x: -248.0035880, x1: -0.2527235, n: 9]
secant: ~[x: -0.2527245, x1: -248.0035880, n: 10]
secant: ~[x: -0.2527256, x1: -0.2527245, n: 11]
secant: ~[x: -247.9974315, x1: -0.2527256, n: 12]
secant: ~[x: -0.2527266, x1: -247.9974315, n: 13]
secant: ~[x: -0.2527277, x1: -0.2527266, n: 14]
secant: ~[x: -247.9912657, x1: -0.2527277, n: 15]
secant: ~[x: -0.2527287, x1: -247.9912657, n: 16]
secant: ~[x: -0.2527298, x1: -0.2527287, n: 17]
secant: ~[x: -247.9850983, x1: -0.2527298, n: 18]
secant: ~[x: -0.2527308, x1: -247.9850983, n: 19]
secant: ~[x: -0.2527319, x1: -0.2527308, n: 20]
secant: ~[x: -247.9789389, x1: -0.2527319, n: 21]
secant: ~[x: -0.2527329, x1: -247.9789389, n: 22]
secant: ~[x: -0.2527340, x1: -0.2527329, n: 23]
secant: ~[x: -247.9727780, x1: -0.2527340, n: 24]
secant: ~[x: -0.2527350, x1: -247.9727780, n: 25]
secant: ~[x: -0.2527361, x1: -0.2527350, n: 26]
secant: ~[x: -247.9666117, x1: -0.2527361, n: 27]
secant: ~[x: -0.2527371, x1: -247.9666117, n: 28]
secant: ~[x: -0.2527381, x1: -0.2527371, n: 29]
secant: ~[x: -247.9604516, x1: -0.2527381, n: 30]
secant: ~[x: -0.2527392, x1: -247.9604516, n: 31]
secant: ~[x: -0.2527402, x1: -0.2527392, n: 32]
secant: ~[x: -247.9542826, x1: -0.2527402, n: 33]
secant: ~[x: -0.2527413, x1: -247.9542826, n: 34]
secant: ~[x: -0.2527423, x1: -0.2527413, n: 35]
secant: ~[x: -247.9481238, x1: -0.2527423, n: 36]
secant: ~[x: -0.2527434, x1: -247.9481238, n: 37]
secant: ~[x: -0.2527444, x1: -0.2527434, n: 38]
secant: ~[x: -247.9419567, x1: -0.2527444, n: 39]
secant: ~[x: -0.2527455, x1: -247.9419567, n: 40]
secant: ~[x: -0.2527465, x1: -0.2527455, n: 41]
secant: ~[x: -247.9357918, x1: -0.2527465, n: 42]
secant: ~[x: -0.2527476, x1: -247.9357918, n: 43]
secant: ~[x: -0.2527486, x1: -0.2527476, n: 44]
secant: ~[x: -247.9296301, x1: -0.2527486, n: 45]
secant: ~[x: -0.2527497, x1: -247.9296301, n: 46]
secant: ~[x: -0.2527507, x1: -0.2527497, n: 47]
secant: ~[x: -247.9234680, x1: -0.2527507, n: 48]
secant: ~[x: -0.2527518, x1: -247.9234680, n: 49]
secant: ~[x: -0.2527528, x1: -0.2527518, n: 50]
secant: ~[x: -247.9173036, x1: -0.2527528, n: 51]
secant: ~[x: -0.2527539, x1: -247.9173036, n: 52]
secant: ~[x: -0.2527549, x1: -0.2527539, n: 53]
secant: ~[x: -247.9111363, x1: -0.2527549, n: 54]
secant: ~[x: -0.2527560, x1: -247.9111363, n: 55]
secant: ~[x: -0.2527570, x1: -0.2527560, n: 56]
secant: ~[x: -247.9049742, x1: -0.2527570, n: 57]
secant: ~[x: -0.2527581, x1: -247.9049742, n: 58]
secant: ~[x: -0.2527591, x1: -0.2527581, n: 59]
secant: ~[x: -247.8988062, x1: -0.2527591, n: 60]
secant: ~[x: -0.2527602, x1: -247.8988062, n: 61]
secant: ~[x: -0.2527612, x1: -0.2527602, n: 62]
secant: ~[x: -247.8926396, x1: -0.2527612, n: 63]
secant: ~[x: -0.2527623, x1: -247.8926396, n: 64]
secant: ~[x: -0.2527633, x1: -0.2527623, n: 65]
secant: ~[x: -247.8864716, x1: -0.2527633, n: 66]
secant: ~[x: -0.2527644, x1: -247.8864716, n: 67]
secant: ~[x: -0.2527654, x1: -0.2527644, n: 68]
secant: ~[x: -247.8803110, x1: -0.2527654, n: 69]
secant: ~[x: -0.2527665, x1: -247.8803110, n: 70]
secant: ~[x: -0.2527675, x1: -0.2527665, n: 71]
secant: ~[x: -247.8741441, x1: -0.2527675, n: 72]
secant: ~[x: -0.2527686, x1: -247.8741441, n: 73]
secant: ~[x: -0.2527696, x1: -0.2527686, n: 74]
secant: ~[x: -247.8679731, x1: -0.2527696, n: 75]
secant: ~[x: -0.2527707, x1: -247.8679731, n: 76]
secant: ~[x: -0.2527717, x1: -0.2527707, n: 77]
secant: ~[x: -247.8618048, x1: -0.2527717, n: 78]
secant: ~[x: -0.2527728, x1: -247.8618048, n: 79]
secant: ~[x: -0.2527738, x1: -0.2527728, n: 80]
secant: ~[x: -247.8556377, x1: -0.2527738, n: 81]
secant: ~[x: -0.2527749, x1: -247.8556377, n: 82]
secant: ~[x: -0.2527759, x1: -0.2527749, n: 83]
secant: ~[x: -247.8494702, x1: -0.2527759, n: 84]
secant: ~[x: -0.2527770, x1: -247.8494702, n: 85]
secant: ~[x: -0.2527780, x1: -0.2527770, n: 86]
secant: ~[x: -247.8433069, x1: -0.2527780, n: 87]
secant: ~[x: -0.2527791, x1: -247.8433069, n: 88]
secant: ~[x: -0.2527801, x1: -0.2527791, n: 89]
secant: ~[x: -247.8371341, x1: -0.2527801, n: 90]
secant: ~[x: -0.2527812, x1: -247.8371341, n: 91]
secant: ~[x: -0.2527822, x1: -0.2527812, n: 92]
secant: ~[x: -247.8309606, x1: -0.2527822, n: 93]
secant: ~[x: -0.2527833, x1: -247.8309606, n: 94]
secant: ~[x: -0.2527843, x1: -0.2527833, n: 95]
secant: ~[x: -247.8247921, x1: -0.2527843, n: 96]
secant: ~[x: -0.2527854, x1: -247.8247921, n: 97]
secant: ~[x: -0.2527864, x1: -0.2527854, n: 98]
secant: ~[x: -247.8186311, x1: -0.2527864, n: 99]
secant: ~[x: -0.2527875, x1: -247.8186311, n: 100]
secant: ~[x: -0.2527885, x1: -0.2527875, n: 101]

bisection: ~[a: -5.0000000, b: 0.0000000, n: 0]
bisection: ~[a: -2.5000000, b: 0.0000000, n: 1]
bisection: ~[a: -2.5000000, b: -1.2500000, n: 2]
bisection: ~[a: -2.5000000, b: -1.8750000, n: 3]
bisection: ~[a: -2.1875000, b: -1.8750000, n: 4]
bisection: ~[a: -2.0312500, b: -1.8750000, n: 5]
bisection: ~[a: -2.0312500, b: -1.9531250, n: 6]
bisection: ~[a: -2.0312500, b: -1.9921875, n: 7]
bisection: ~[a: -2.0117188, b: -1.9921875, n: 8]
bisection: ~[a: -2.0019531, b: -1.9921875, n: 9]
bisection: ~[a: -2.0019531, b: -1.9970703, n: 10]
bisection: ~[a: -2.0019531, b: -1.9995117, n: 11]
bisection: ~[a: -2.0007324, b: -1.9995117, n: 12]
bisection: ~[a: -2.0001221, b: -1.9995117, n: 13]
bisection: ~[a: -2.0001221, b: -1.9998169, n: 14]
bisection: ~[a: -2.0001221, b: -1.9999695, n: 15]
bisection: ~[a: -2.0000458, b: -1.9999695, n: 16]
bisection: ~[a: -2.0000076, b: -1.9999695, n: 17]
bisection: ~[a: -2.0000076, b: -1.9999886, n: 18]
bisection: ~[a: -2.0000076, b: -1.9999981, n: 19]
bisection: ~[a: -2.0000029, b: -1.9999981, n: 20]
bisection: ~[a: -2.0000005, b: -1.9999981, n: 21]
bisection: ~[a: -2.0000005, b: -1.9999993, n: 22]
bisection: ~[a: -2.0000005, b: -1.9999999, n: 23]
bisection: ~[a: -2.0000002, b: -1.9999999, n: 24]
bisection: ~[a: -2.0000000, b: -1.9999999, n: 25]
bisection: ~[a: -2.0000000, b: -2.0000000, n: 26]

newton: ~[x: -2.5000000, n: 0]
newton: ~[x: -2.1310000, n: 1]
newton: ~[x: -2.0115921, n: 2]
newton: ~[x: -2.0000998, n: 3]
newton: ~[x: -2.0000000, n: 4]
newton: ~[x: -2.0000000, n: 5]

finding root of x^10 - 1 in [0.9000000, 2.0000000]
secant: ~[x: 0.9000000, x1: 2.0000000, n: 0]
secant: ~[x: 0.9006999, x1: 0.9000000, n: 1]
secant: ~[x: 1.0675300, x1: 0.9006999, n: 2]
secant: ~[x: 0.9695854, x1: 1.0675300, n: 3]
secant: ~[x: 0.9914941, x1: 0.9695854, n: 4]
secant: ~[x: 1.0012512, x1: 0.9914941, n: 5]
secant: ~[x: 0.9999515, x1: 1.0012512, n: 6]
secant: ~[x: 0.9999997, x1: 0.9999515, n: 7]
secant: ~[x: 1.0000000, x1: 0.9999997, n: 8]

bisection: ~[a: 0.9000000, b: 2.0000000, n: 0]
bisection: ~[a: 0.9000000, b: 1.4500000, n: 1]
bisection: ~[a: 0.9000000, b: 1.1750000, n: 2]
bisection: ~[a: 0.9000000, b: 1.0375000, n: 3]
bisection: ~[a: 0.9687500, b: 1.0375000, n: 4]
bisection: ~[a: 0.9687500, b: 1.0031250, n: 5]
bisection: ~[a: 0.9859375, b: 1.0031250, n: 6]
bisection: ~[a: 0.9945313, b: 1.0031250, n: 7]
bisection: ~[a: 0.9988281, b: 1.0031250, n: 8]
bisection: ~[a: 0.9988281, b: 1.0009766, n: 9]
bisection: ~[a: 0.9999023, b: 1.0009766, n: 10]
bisection: ~[a: 0.9999023, b: 1.0004395, n: 11]
bisection: ~[a: 0.9999023, b: 1.0001709, n: 12]
bisection: ~[a: 0.9999023, b: 1.0000366, n: 13]
bisection: ~[a: 0.9999695, b: 1.0000366, n: 14]
bisection: ~[a: 0.9999695, b: 1.0000031, n: 15]
bisection: ~[a: 0.9999863, b: 1.0000031, n: 16]
bisection: ~[a: 0.9999947, b: 1.0000031, n: 17]
bisection: ~[a: 0.9999989, b: 1.0000031, n: 18]
bisection: ~[a: 0.9999989, b: 1.0000010, n: 19]
bisection: ~[a: 0.9999999, b: 1.0000010, n: 20]
bisection: ~[a: 0.9999999, b: 1.0000004, n: 21]
bisection: ~[a: 0.9999999, b: 1.0000002, n: 22]
bisection: ~[a: 0.9999999, b: 1.0000000, n: 23]
bisection: ~[a: 1.0000000, b: 1.0000000, n: 24]

newton: ~[x: 1.4500000, n: 0]
newton: ~[x: 1.3085293, n: 1]
newton: ~[x: 1.1865673, n: 2]
newton: ~[x: 1.0893577, n: 3]
newton: ~[x: 1.0267096, n: 4]
newton: ~[x: 1.0029195, n: 5]
newton: ~[x: 1.0000379, n: 6]
newton: ~[x: 1.0000000, n: 7]

finding root of x^10 - 1 in [-0.9000000, -2.0000000]
secant: ~[x: -0.9000000, x1: -2.0000000, n: 0]
secant: ~[x: -0.9006999, x1: -0.9000000, n: 1]
secant: ~[x: -1.0675300, x1: -0.9006999, n: 2]
secant: ~[x: -0.9695854, x1: -1.0675300, n: 3]
secant: ~[x: -0.9914941, x1: -0.9695854, n: 4]
secant: ~[x: -1.0012512, x1: -0.9914941, n: 5]
secant: ~[x: -0.9999515, x1: -1.0012512, n: 6]
secant: ~[x: -0.9999997, x1: -0.9999515, n: 7]
secant: ~[x: -1.0000000, x1: -0.9999997, n: 8]

bisection: ~[a: -0.9000000, b: -2.0000000, n: 0]
bisection: ~[a: -0.9000000, b: -1.4500000, n: 1]
bisection: ~[a: -0.9000000, b: -1.1750000, n: 2]
bisection: ~[a: -0.9000000, b: -1.0375000, n: 3]
bisection: ~[a: -0.9687500, b: -1.0375000, n: 4]
bisection: ~[a: -0.9687500, b: -1.0031250, n: 5]
bisection: ~[a: -0.9859375, b: -1.0031250, n: 6]
bisection: ~[a: -0.9945313, b: -1.0031250, n: 7]
bisection: ~[a: -0.9988281, b: -1.0031250, n: 8]
bisection: ~[a: -0.9988281, b: -1.0009766, n: 9]
bisection: ~[a: -0.9999023, b: -1.0009766, n: 10]
bisection: ~[a: -0.9999023, b: -1.0004395, n: 11]
bisection: ~[a: -0.9999023, b: -1.0001709, n: 12]
bisection: ~[a: -0.9999023, b: -1.0000366, n: 13]
bisection: ~[a: -0.9999695, b: -1.0000366, n: 14]
bisection: ~[a: -0.9999695, b: -1.0000031, n: 15]
bisection: ~[a: -0.9999863, b: -1.0000031, n: 16]
bisection: ~[a: -0.9999947, b: -1.0000031, n: 17]
bisection: ~[a: -0.9999989, b: -1.0000031, n: 18]
bisection: ~[a: -0.9999989, b: -1.0000010, n: 19]
bisection: ~[a: -0.9999999, b: -1.0000010, n: 20]
bisection: ~[a: -0.9999999, b: -1.0000004, n: 21]
bisection: ~[a: -0.9999999, b: -1.0000002, n: 22]
bisection: ~[a: -0.9999999, b: -1.0000000, n: 23]
bisection: ~[a: -1.0000000, b: -1.0000000, n: 24]

newton: ~[x: -1.4500000, n: 0]
newton: ~[x: -1.3085293, n: 1]
newton: ~[x: -1.1865673, n: 2]
newton: ~[x: -1.0893577, n: 3]
newton: ~[x: -1.0267096, n: 4]
newton: ~[x: -1.0029195, n: 5]
newton: ~[x: -1.0000379, n: 6]
newton: ~[x: -1.0000000, n: 7]

finding root of tanh(x) - 1 in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]

bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]

newton: ~[x: 0.0000000, n: 0]

finding root of tanh(x) - x^10 in [-0.1000000, 0.1000000]
secant: ~[x: -0.1000000, x1: 0.1000000, n: 0]
secant: ~[x: 0.0000000, x1: -0.1000000, n: 1]

bisection: ~[a: -0.1000000, b: 0.1000000, n: 0]
bisection: ~[a: -0.1000000, b: 0.0000000, n: 1]
bisection: ~[a: -0.0500000, b: 0.0000000, n: 2]
bisection: ~[a: -0.0250000, b: 0.0000000, n: 3]
bisection: ~[a: -0.0125000, b: 0.0000000, n: 4]
bisection: ~[a: -0.0062500, b: 0.0000000, n: 5]
bisection: ~[a: -0.0031250, b: 0.0000000, n: 6]
bisection: ~[a: -0.0015625, b: 0.0000000, n: 7]
bisection: ~[a: -0.0007813, b: 0.0000000, n: 8]
bisection: ~[a: -0.0003906, b: 0.0000000, n: 9]
bisection: ~[a: -0.0001953, b: 0.0000000, n: 10]
bisection: ~[a: -0.0000977, b: 0.0000000, n: 11]
bisection: ~[a: -0.0000488, b: 0.0000000, n: 12]
bisection: ~[a: -0.0000244, b: 0.0000000, n: 13]
bisection: ~[a: -0.0000122, b: 0.0000000, n: 14]
bisection: ~[a: -0.0000061, b: 0.0000000, n: 15]
bisection: ~[a: -0.0000031, b: 0.0000000, n: 16]
bisection: ~[a: -0.0000015, b: 0.0000000, n: 17]
bisection: ~[a: -0.0000008, b: 0.0000000, n: 18]
bisection: ~[a: -0.0000004, b: 0.0000000, n: 19]
bisection: ~[a: -0.0000002, b: 0.0000000, n: 20]
bisection: ~[a: -0.0000001, b: 0.0000000, n: 21]

newton: ~[x: 0.0000000, n: 0]

finding root of tanh(x) - x^10 in [0.9000000, 1.1000000]
secant: ~[x: 0.9000000, x1: 1.1000000, n: 0]
secant: ~[x: 0.9340252, x1: 0.9000000, n: 1]
secant: ~[x: 0.9890291, x1: 0.9340252, n: 2]
secant: ~[x: 0.9681836, x1: 0.9890291, n: 3]
secant: ~[x: 0.9712793, x1: 0.9681836, n: 4]
secant: ~[x: 0.9715674, x1: 0.9712793, n: 5]
secant: ~[x: 0.9715626, x1: 0.9715674, n: 6]

bisection: ~[a: 0.9000000, b: 1.1000000, n: 0]
bisection: ~[a: 0.9000000, b: 1.0000000, n: 1]
bisection: ~[a: 0.9500000, b: 1.0000000, n: 2]
bisection: ~[a: 0.9500000, b: 0.9750000, n: 3]
bisection: ~[a: 0.9625000, b: 0.9750000, n: 4]
bisection: ~[a: 0.9687500, b: 0.9750000, n: 5]
bisection: ~[a: 0.9687500, b: 0.9718750, n: 6]
bisection: ~[a: 0.9703125, b: 0.9718750, n: 7]
bisection: ~[a: 0.9710938, b: 0.9718750, n: 8]
bisection: ~[a: 0.9714844, b: 0.9718750, n: 9]
bisection: ~[a: 0.9714844, b: 0.9716797, n: 10]
bisection: ~[a: 0.9714844, b: 0.9715820, n: 11]
bisection: ~[a: 0.9715332, b: 0.9715820, n: 12]
bisection: ~[a: 0.9715576, b: 0.9715820, n: 13]
bisection: ~[a: 0.9715576, b: 0.9715698, n: 14]
bisection: ~[a: 0.9715576, b: 0.9715637, n: 15]
bisection: ~[a: 0.9715607, b: 0.9715637, n: 16]
bisection: ~[a: 0.9715622, b: 0.9715637, n: 17]
bisection: ~[a: 0.9715622, b: 0.9715630, n: 18]
bisection: ~[a: 0.9715626, b: 0.9715630, n: 19]
bisection: ~[a: 0.9715626, b: 0.9715628, n: 20]
bisection: ~[a: 0.9715626, b: 0.9715627, n: 21]

newton: ~[x: 1.0000000, n: 0]
newton: ~[x: 0.9751143, n: 1]
newton: ~[x: 0.9716242, n: 2]
newton: ~[x: 0.9715626, n: 3]
newton: ~[x: 0.9715626, n: 4]
'''
