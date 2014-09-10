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
from math import sqrt, pi

# a)

def pathlength(pts):
    L = 0
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        L += sqrt(dx**2 + dy**2)
    return L

# b)

def test_pathlength():
    # Simple test
    t = pathlength([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    print 'Simple test OK?', t == 4.0

    # Compute Pi and check
    f = lambda x: sqrt(1 - x**2)
    pts = []
    COUNT = 10000
    for i in range(0, COUNT):
        x = -1.0 + 1.0 * i / (COUNT - 1.0)
        pt = [x, f(x)]
        pts.append(pt)
    eps = pi / 2 - pathlength(pts)
    print 'Pi OK?', eps < 1e-6


def main():
    'entry point'
    test_pathlength()

if __name__ == '__main__':
    main()

