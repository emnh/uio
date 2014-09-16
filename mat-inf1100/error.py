#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>

from random import random

def main():
    'entry point'
    antfeil = 0; N = 10000
    x0 = y0 = z0 = 0.0
    feilass1 = feilass2 = 0.0

    for i in range(N):
        x = random(); y = random(); z = random();
        ass1 = (x + y + z)**2
        ass2 = x**2 + y**2 + z**2 + 2*x*y + 2*x*z + 2*y*z

        if ass1 != ass2:
            antfeil += 1
            x0 = x; y0 = y; z0 = z
            feilass1 = ass1
            feilass2 = ass2
    print (100. * antfeil / N)
    print x0, y0, z0, feilass1 - feilass2

if __name__ == '__main__':
    main()

