#!/usr/bin/env python

import sys
from math import sqrt
import decimal

def task_a():
    print 'Give a, b and c on separate lines'
    [a, b, c] = [float(x) for x in sys.stdin.readlines()]

    q = b*b - 4*a*c
    q_sr = sqrt(q)
    x1 = (-b - q_sr) / (2 * a)
    x2 = (-b + q_sr) / (2 * a)
    print x1, x2

    # Run example
    '''
    Give a, b and c on separate lines
    1
    8
    4
    -0.535898384862 -7.46410161514
    '''

    # Run example
    '''
    Give a, b and c on separate lines
    1
    5
    6
    -2.0 -3.0
    '''

    # Run example
    '''
    Give a, b and c on separate lines
    1
    -4
    -21
    7.0 -3.0
    '''

def task_b():
    # Run example
    '''
    Give a, b and c on separate lines
    1e-6
    10
    1e-6
    -10000000.0 -9.94759830064e-08
    '''

def task_decimal():
    print 'Give a, b and c on separate lines'
    [a, b, c] = [decimal.Decimal(x) for x in sys.stdin.readlines()]

    q = b*b - 4*a*c
    q_sr = q.sqrt() # decimal.sqrt(q)
    x1 = (-b - q_sr) / (2 * a)
    x2 = (-b + q_sr) / (2 * a)
    print x1, x2

if __name__ == '__main__':
    task_a()
    #task_decimal()
