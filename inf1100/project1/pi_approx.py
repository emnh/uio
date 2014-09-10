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
import pathlength
from math import sqrt, pi, cos, sin

def compute_pi(n):
   # Compute Pi and check
    fx = lambda i: cos(2*i*pi/n) / 2.0
    fy = lambda i: sin(2*i*pi/n) / 2.0
    pts = []
    for i in range(0, n + 1):
        x = fx(i)
        y = fy(i)
        pt = [x, y]
        pts.append(pt)
    eps = pi - pathlength.pathlength(pts)
    print 'Pi error', eps

def main():
    'entry point'
    for n in [2**k for k in range(2, 10+1)]:
        compute_pi(n)

if __name__ == '__main__':
    main()

