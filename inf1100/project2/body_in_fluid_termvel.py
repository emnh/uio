#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

from body_in_fluid import FluidBody
from math import pi, sqrt, copysign
from ODESolver import ForwardEuler
from matplotlib.pylab import *
import numpy

class TermFluidBody(FluidBody):
    # E.8 a)
    def term_velocity(self):
        globals().update(self.__dict__)
        inner = -2.0 * g * (1 - sigma / sigma_b) / (C_D * sigma * A) * (sigma_b * V)
        sgn = copysign(1.0, inner)
        uk = sgn * sqrt(abs(inner))
        return uk

def getEPSCheck(steps):
    def epsilonCheck(u, t, step_no):
        eps = 1.0E-30
        #print u[-1], u[-2]
        # eps check doesn't work, just compute by steps, we have the array anyway
        retval = step_no >= steps # and (u[-1] - u[-2]) < eps
        return retval
    return epsilonCheck

# a) Run example
'''
skydiver terminal velocity -60.7244283837
ball terminal velocity 3.64394135531
'''

# b)
# c) d)
# The graph converges to a value a bit different than the exact, possibly a floating point issue.
def term_velocity_skydiver():
    fb = TermFluidBody(0.79, 1003.0, 0.9, 0.08, 0.6)
    termvel = fb.term_velocity()

    nvals = range(10, 10000, 100)
    numerical_termvels = []
    for N in nvals:
        fe = ForwardEuler(fb)
        fe.set_initial_condition(0.0)
        tvals = numpy.linspace(0.0, 30.0, N)
        numerical_termvel = fe.solve(tvals, terminate=getEPSCheck(N))
        numerical_termvel = numerical_termvel[0][-1]
        numerical_termvels.append(numerical_termvel)
    print 'skydiver terminal velocity exact %.7f numerical %.7f', termvel, numerical_termvel
    plot(nvals, [termvel for x in nvals])
    plot(nvals, numerical_termvels)
    show()

# b)
# c) e)
# The graph converges very well.
def term_velocity_ball():
    r = 0.11
    m = 0.43
    V = 4.0/3.0*pi*r**3
    sigma_b = m / V
    fb = TermFluidBody(sigma=1000.0, sigma_b=sigma_b, A=pi*r**2, V=V, C_D=0.2)
    termvel = fb.term_velocity()

    nvals = range(10, 10000, 100)
    numerical_termvels = []
    for N in nvals:
        fe = ForwardEuler(fb)
        fe.set_initial_condition(0.0)
        tvals = numpy.linspace(0.0, 30.0, N)
        numerical_termvel = fe.solve(tvals, terminate=getEPSCheck(N))
        numerical_termvel = numerical_termvel[0][-1]
        numerical_termvels.append(numerical_termvel)
    print 'ball terminal velocity exact %.7f numerical %.7f', termvel, numerical_termvel
    plot(nvals, [termvel for x in nvals])
    plot(nvals, numerical_termvels)
    show()

def main():
    'entry point'
    term_velocity_skydiver()
    term_velocity_ball()

if __name__ == '__main__':
    main()

