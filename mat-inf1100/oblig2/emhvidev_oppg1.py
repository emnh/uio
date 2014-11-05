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
from matplotlib.pylab import *

def accel(t, v):
    al = []
    al.append(0)
    for i in range(1, len(v)):
        dt = t[i] - t[i - 1]
        a = (v[i] - v[i - 1]) / dt
        al.append(a)
    return al

def dist(t, v):
    sl = []
    s = 0
    sl.append(s)
    for i in range(1, len(v)):
        dt = t[i] - t[i - 1]
        s += v[i] * dt
        sl.append(s)
    return sl

def readfile():
    t = []
    v = []
    infile = file('running.txt', 'r')
    for line in infile:
        tnext, vnext = line.strip().split(',')
        t.append(float(tnext))
        v.append(float(vnext))
    infile.close()
    return [t, v]

def main():
    'entry point'
    [t, v] = readfile()
    a = accel(t, v)
    s = dist(t, v)
    plot(t, a)
    show()
    plot(t, s)
    show()



if __name__ == '__main__':
    main()

