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
from sinesum2 import table
import argparse

def main():
    'entry point'
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-T', metavar='T', type=float,
                   help='T value for Fourier table')
    parser.add_argument('-n', metavar='n', type=int, nargs='+',
                   help='n values for Fourier table')
    parser.add_argument('-alpha', metavar='alpha', type=float, nargs='+',
                   help='alpha values for Fourier table')
    args = parser.parse_args()
    table(args.n, args.alpha, args.T)
    #print args.T
    #print args.n
    #print args.alpha

if __name__ == '__main__':
    main()

# Run example
'''
emhvidev@vetur ~/www_docs/inf1100/project1 1% ./sinesum3.py -T 6.28 -n 1 3 5 10 30 100 -alpha 0.01 0.25 0.49
n 1 alpha 0.01 S(t, n, T) - f(t, T) -0.920052627501
n 3 alpha 0.01 S(t, n, T) - f(t, T) -0.761834996162
n 5 alpha 0.01 S(t, n, T) - f(t, T) -0.608585435311
n 10 alpha 0.01 S(t, n, T) - f(t, T) -0.266797434877
n 30 alpha 0.01 S(t, n, T) - f(t, T) 0.14481610778
n 100 alpha 0.01 S(t, n, T) - f(t, T) -0.050094008341
n 1 alpha 0.25 S(t, n, T) - f(t, T) 0.273239544735
n 3 alpha 0.25 S(t, n, T) - f(t, T) 0.103474272104
n 5 alpha 0.25 S(t, n, T) - f(t, T) 0.0630539690963
n 10 alpha 0.25 S(t, n, T) - f(t, T) -0.0317523771092
n 30 alpha 0.25 S(t, n, T) - f(t, T) -0.0106073863054
n 100 alpha 0.25 S(t, n, T) - f(t, T) -0.00318301929431
n 1 alpha 0.49 S(t, n, T) - f(t, T) -0.920052627501
n 3 alpha 0.49 S(t, n, T) - f(t, T) -0.761834996162
n 5 alpha 0.49 S(t, n, T) - f(t, T) -0.608585435311
n 10 alpha 0.49 S(t, n, T) - f(t, T) -0.266797434877
n 30 alpha 0.49 S(t, n, T) - f(t, T) 0.14481610778
n 100 alpha 0.49 S(t, n, T) - f(t, T) -0.050094008341
'''
