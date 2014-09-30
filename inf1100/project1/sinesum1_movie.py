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
#from matplotlib.pylab import *
from math import pi
from scitools.std import plot, movie
from sinesum2 import S, f

def main():
    'entry point'
    T = 2*pi
    xl = np.linspace(0.01, T-0.01, 100)
    tl = [x for x in xl]
    y = [f(t, T) for t in tl]
    counter = 0
    filename = 'tmp_'
    for n in [1, 3, 20, 200]:
        yp = [S(t, n, T) for t in tl]
        #plot(tl, y)
        plot(tl, y, tl, yp, savefig='%s%04d.png' % (filename, counter))
        counter += 1
    movie('tmp*.png', encoder='convert', fps=2, output_file='sinesum.gif')

if __name__ == '__main__':
    main()


# Run example
'''
emhvidev@vetur ~/www_docs/inf1100/project1 1% ./sinesum1_movie.py                                                                                                                                     :(



Found 4 files of the format tmp*.png.

scitools.easyviz.movie function runs the command:

    convert -delay 50 tmp*.png sinesum.gif



    movie in output file sinesum.gif
    ./sinesum1_movie.py  3.88s user 2.25s system 61% cpu 10.000 total

'''
