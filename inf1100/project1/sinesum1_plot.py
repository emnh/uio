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
import numpy as np
from matplotlib.pylab import *
from sinesum2 import S, f

def main():
    'entry point'
    T = 2*pi
    xl = np.linspace(0.01, T-0.01, 100)
    tl = [x for x in xl]
    y = [f(t, T) for t in tl]
    plot(tl, y)
    for n in [1, 3, 20, 200]:
        yp = [S(t, n, T) for t in tl]
        plot(tl, yp)
    show()

if __name__ == '__main__':
    main()

# Run example.
# Only graphical output.
