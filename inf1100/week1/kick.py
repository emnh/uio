#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

from math import pi

'''
kick.py
Oblig2 Week2 INF1100 H2014
'''

def F_d(C_D, rho, A, V):
    return 0.5 * C_D * rho * A * V**2

def print_F_d(C_D, rho, A, V, m, g):
    F_g = m * g
    F_drag = F_d(C_D, rho, A, V)
    print 'V = %.2f m/s' % V
    print 'Drag force: %.2f kgm/s**2' % F_drag
    print 'Drag force / grav force: %.2f' % (F_drag / F_g)

def main():
    'entry point'
    C_D = 0.2     # coefficient
    rho = 1.2     # kg/m**3
    a = 0.11      # m
    m = 0.43      # kg
    V1 = 120      # km / h
    V2 = 10       # km / h
    g = 9.81      # m / s**2
    A = pi * a**2 # m**2
    F_d1 = print_F_d(C_D, rho, A, V1, m, g)
    F_d2 = print_F_d(C_D, rho, A, V2, m, g)

if __name__ == '__main__':
    main()

# Run example
'''
V = 120.00 m/s
Drag force: 65.69 kgm/s**2
Drag force / grav force: 15.57
V = 10.00 m/s
Drag force: 0.46 kgm/s**2
Drag force / grav force: 0.11
'''
