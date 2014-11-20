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

import numpy
import ODESolver
from matplotlib.pylab import *

class ProblemSIR:
    def __init__(self, nu, beta, S0, I0, R0, T):
        self.T = T
        self.S0 = S0
        self.I0 = I0
        self.R0 = R0

        if isinstance(nu, (float, int)):
            self.nu = lambda t: nu
        elif callable(nu):
            self.nu = nu

        if isinstance(beta, (float, int)):
            self.beta = lambda t: beta
        elif callable(beta):
            self.beta = beta

    def __call__(self, u, t):
        S, I, R = u
        return [
                -self.beta(t)*S*I,
                self.beta(t)*S*I-self.nu(t)*I,
                self.nu(t)*I]

    def term(self, u, t, i):
        S, I, R = u[i]
        eps = 1e-7
        return S + I + R - (self.S0 + self.I0 + self.R0) > eps

class SolverSIR:
    def __init__(self, problem, dt):
        self.problem = problem
        self.dt = dt

    def solve(self, method=ODESolver.RungeKutta4):
        'entry point'
        problem = self.problem
        solver = method(problem)
        solver.set_initial_condition([problem.S0, problem.I0, problem.R0])
        n = int(round(self.problem.T/float(self.dt)))
        tp = numpy.linspace(0, self.problem.T, n)
        u, t = solver.solve(tp, lambda u, t, i: problem.term(u, t, i))
        print max(u[:,1])
        return tp, u[:,0], u[:,1], u[:,2]

def doPlot(tp, a, b, c):
    plot(tp, a, 'r-')
    plot(tp, b, 'g-')
    plot(tp, c, 'b-')
    show()

def main():
    beta = lambda t: 0.0005 if t <= 12 else 0.0001
    problem = ProblemSIR(T=60, nu=0.1, beta=beta, S0=1500, I0=1.0, R0=0.0)
    solver = SolverSIR(problem, 0.5)
    tp, a, b, c = solver.solve()
    doPlot(tp, a, b, c)


if __name__ == '__main__':
    main()

'''
The total number of infected is now 744.88 compared to ~897.18 for beta = 0.0005.
'''
