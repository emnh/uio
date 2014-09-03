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

    # Print them
    for tv, yv in zip(t, y):
        print tv, yv

if __name__ == '__main__':
    main()

# Run example
'''
0.0 0.0
0.142711518858 0.899082568807
0.285423037717 1.59836901121
0.428134556575 2.09785932722
0.570846075433 2.39755351682
0.713557594292 2.49745158002
0.85626911315 2.39755351682
0.998980632008 2.09785932722
1.14169215087 1.59836901121
1.28440366972 0.899082568807
1.42711518858 0.0
'''
