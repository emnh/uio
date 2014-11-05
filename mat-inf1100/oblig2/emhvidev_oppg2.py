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
from math import sqrt, tan, pi
from matplotlib.pylab import *

def forwardEuler(f, N, T, uk):
    dt = float(T) / N
    for i in range(N+1):
        tk = i * dt
        yield [tk, uk]
        uk = uk + dt * f(uk, tk)

def midpointEuler(f, N, T, uk):
    dt = float(T) / N
    for i in range(N+1):
        tk = i * dt
        yield [tk, uk]
        uk12 = uk + dt*f(uk, tk)/2.0
        uk = uk + dt*f(uk12, tk + dt/2.0)

def customSolution(f, N, T, uk):
    dt = float(T) / N
    for i in range(N+1):
        tk = i * dt
        yield [tk, uk]
        uk = (2 - dt*uk - 2 * sqrt(1 - dt**2 - 2*uk*dt)) / dt

def plot_compare_b():
    f = lambda uk, tk: 1.0 + uk**2
    f_exact = lambda t: tan(t + pi/4.0)
    T = 0.6
    N = 6
    uk_start = 1.0
    tks = []
    uks = []
    exacts = []
    for [tk, uk] in forwardEuler(f, N, T, uk_start):
        tks.append(tk)
        uks.append(uk)
        exact = f_exact(tk)
        exacts.append(exact)
        print tk, uk, exact
    plot(tks, uks)
    plot(tks, exacts)
    show()

def plot_compare_c():
    f = lambda uk, tk: 1.0 + uk**2
    f_exact = lambda t: tan(t + pi/4.0)
    T = 0.6
    N = 6
    uk_start = 1.0
    tks = []
    uks = []
    uks_mid = []
    exacts = []
    for [tk, uk] in forwardEuler(f, N, T, uk_start):
        tks.append(tk)
        uks.append(uk)
        exact = f_exact(tk)
        exacts.append(exact)
        print tk, uk, exact
    print
    i = 0
    for [tk, uk] in midpointEuler(f, N, T, uk_start):
        uks_mid.append(uk)
        print tk, uks[i], uk
        i += 1
    plot(tks, uks)
    plot(tks, uks_mid)
    plot(tks, exacts)
    show()

def plot_compare_d():
    f = lambda uk, tk: 1.0 + uk**2
    f_exact = lambda t: tan(t + pi/4.0)
    T = 0.6
    N = 6
    uk_start = 1.0
    tks = []
    uks = []
    uks_mid = []
    uks_custom = []
    exacts = []
    for [tk, uk] in forwardEuler(f, N, T, uk_start):
        tks.append(tk)
        uks.append(uk)
        exact = f_exact(tk)
        exacts.append(exact)
        print tk, uk, exact
    print

    i = 0
    for [tk, uk] in midpointEuler(f, N, T, uk_start):
        uks_mid.append(uk)
        print tk, uks[i], uk
        i += 1
    print

    i = 0
    for [tk, uk] in customSolution(f, N, T, uk_start):
        uks_custom.append(uk)
        print tk, uks[i], uk
        i += 1
    plot(tks, uks)
    plot(tks, uks_mid)
    plot(tks, uks_custom)
    plot(tks, exacts)
    show()

def main():
    'entry point'
    plot_compare_d()

if __name__ == '__main__':
    main()

