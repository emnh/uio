#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

def y_fn(t, v0, g):
    return v0 * t - (g * t**2) / 2

def main():
    n = 10
    v0 = 7.0
    g = 9.81
    maxv = 2 * v0 / g
    t = []
    y = []

    # Calculate the values in lists
    for i in range(0, n + 1):
        normi = i / float(n)
        linval = maxv * normi
        t.append(linval)
        y.append(y_fn(linval, v0, g))

    ty1 = [t, y]
    ty2 = [x for x in zip(t, y)]

    # a) Print from ty1
    print "Printing from column-based list ty1"
    for tv, yv in zip(*ty1):
        print '%.2f %.2f' % (tv, yv)
    print

    # b) Print from ty1
    print "Printing from row-based list ty2"
    for tv, yv in ty2:
        print '%.2f %.2f' % (tv, yv)

if __name__ == '__main__':
    main()

# Run example
'''
Printing from column-based list ty1
0.00 0.00
0.14 0.90
0.29 1.60
0.43 2.10
0.57 2.40
0.71 2.50
0.86 2.40
1.00 2.10
1.14 1.60
1.28 0.90
1.43 0.00

Printing from row-based list ty2
0.00 0.00
0.14 0.90
0.29 1.60
0.43 2.10
0.57 2.40
0.71 2.50
0.86 2.40
1.00 2.10
1.14 1.60
1.28 0.90
1.43 0.00
'''
