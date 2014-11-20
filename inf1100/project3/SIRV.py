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
    def __init__(self, p, nu, beta, S0, I0, R0, V0, T):
        self.T = T
        self.p = p
        self.S0 = S0
        self.I0 = I0
        self.R0 = R0
        self.V0 = V0

        if isinstance(nu, (float, int)):
            self.nu = lambda t: nu
        elif callable(nu):
            self.nu = nu

        if isinstance(beta, (float, int)):
            self.beta = lambda t: beta
        elif callable(beta):
            self.beta = beta

    def __call__(self, u, t):
        S, I, R, V = u
        return [
                -self.beta(t)*S*I - self.p*S,
                self.beta(t)*S*I-self.nu(t)*I,
                self.nu(t)*I,
                self.p*S]

    def term(self, u, t, i):
        S, I, R, V = u[i]
        eps = 1e-7
        return S + I + R + V - (self.S0 + self.I0 + self.R0 + self.V0) > eps

class SolverSIR:
    def __init__(self, problem, dt):
        self.problem = problem
        self.dt = dt

    def solve(self, method=ODESolver.RungeKutta4):
        'entry point'
        problem = self.problem
        solver = method(problem)
        solver.set_initial_condition([problem.S0, problem.I0, problem.R0, problem.V0])
        n = int(round(self.problem.T/float(self.dt)))
        tp = numpy.linspace(0, self.problem.T, n)
        u, t = solver.solve(tp, lambda u, t, i: problem.term(u, t, i))
        print 'Max infected', max(u[:,1])
        return tp, u[:,0], u[:,1], u[:,2]

def doPlot(tp, a, b, c):
    plot(tp, a, 'r-')
    plot(tp, b, 'g-')
    plot(tp, c, 'b-')
    show()

def main():
    beta = lambda t: 0.0001
    problem = ProblemSIR(T=60, p=0.1, nu=0.1, beta=beta, S0=1500, I0=1.0, R0=0.0, V0=0.0)
    solver = SolverSIR(problem, 0.5)
    tp, a, b, c = solver.solve()
    doPlot(tp, a, b, c)


if __name__ == '__main__':
    main()

'''
Max infected 64.52 with beta = 0.0005. Much less than before with 897.18.
Max infected 1.10 with beta = 0.0001.
'''
