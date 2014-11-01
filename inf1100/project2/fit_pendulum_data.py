#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import re
import numpy as np
from matplotlib.pylab import *

def readData():
    lines = file('pendulum.dat').readlines()[1:]
    xs = []
    ys = []
    for line in lines:
        x, y = re.split(' +', line)
        x = float(x)
        y = float(y)
        xs.append(x)
        ys.append(y)
    xs = np.array(xs)
    ys = np.array(ys)
    return [xs, ys]

# a)
def plot_pendulum():
    [x, y] = readData()
    plot(x, y, 'ro')
    show()

def plot_fit():
    [x, y] = readData()
    plot(x, y, 'ro')
    colors = ['', 'b', 'g', 'y']
    for deg in [1, 2, 3]:
        coeff = polyfit(x, y, deg)
        p = poly1d(coeff)
        y_fitted = p(x)
        plot(x, y_fitted, colors[deg] + '-')
    show()

def main():
    'entry point'
    plot_fit()

if __name__ == '__main__':
    main()

# Run example
# Only graphical output.
