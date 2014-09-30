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
import random
from math import e, pi, log as ln, sin, cos, sinh, tan


# a)

def power3_identity(A=-100, B=100, n=1000):
    err = 0
    for i in range(n):
        a = random.uniform(A, B)
        b = random.uniform(A, B)
        rs = [(a*b)**3, (a**3)*(b**3)]
        if rs[0] != rs[1]:
            err += 1
    return float(err) / n

def test_a():
    print power3_identity()

# b)

def equal(expr1, expr2, A=-100, B=100, n=1000):
    err = 0
    valid = 0
    for i in range(n):
        a = random.uniform(A, B)
        b = random.uniform(A, B)
        try:
            rs0 = eval(expr1)
        except ValueError:
            rs0 = None
        try:
            rs1 = eval(expr2)
        except ValueError:
            rs1 = None
        if rs0 != None and rs1 != None:
            if rs0 != rs1:
                err += 1
            valid += 1
    return float(err) / valid

def test_b():
    print equal("(a*b)**3", "a**3*b**3")
    print equal("e**(a+b)", "e**a*e**b")
    print equal("ln(a**b)", "b*ln(a)")

# c)
'''
Identities:
a − b and −(b − a)
• a/b and 1/(b/a)
• (ab)4 and a4b4
• (a + b)2 and a2 + 2ab + b2
• (a + b)(a − b) and a2 − b2
• ea+b and eaeb
• ln ab and b ln a
• ln ab and ln a + ln b
• ab and eln a+ln b
• 1/(1/a + 1/b) and ab/(a + b)
• a(sin2 b + cos2 b) and a
• sinh(a + b) and (eaeb − e−ae−b)/2
• tan(a + b) and sin(a + b)/ cos(a + b)
• sin(a + b) and sin a cos b + sin b cos a
'''

def test_c():
    idents = [
            ['a - b', '-(b - a)'],
            ['a / b', '1 / (b / a)'],
            ['(a*b)**4', 'a**4*b**4'],
            ['(a + b)**2', 'a**2 + 2*a*b + b**2'],
            ['(a + b)*(a - b)', 'a**2 - b**2'],
            ['e**(a + b)', 'e**a*e**b'],
            ["ln(a**b)", "b*ln(a)"],
            ["ln(a*b)", "ln(a)+ln(b)"],
            ["a*b", "e**(ln(a)+ln(b))"],
            ["1/(1/a+1/b)", "(a*b)/(a + b)"],
            ["a*((sin(b))**2+(cos(b))**2)", "a"],
            ["sinh(a + b)", "(e**a*e**b - e**(-a)*e**(-b))/2"],
            ["tan(a + b)", "sin(a + b)/cos(a + b)"],
            ["sin(a + b)", "sin(a)*cos(b)+sin(b)*cos(a)"]
            ]
    #maxlen = max(max(len(x), len(y)) for x, y in idents)
    #print maxlen
    fd = file('identities_failures.txt', 'w')
    for x, y in idents:
        print >>fd, '[1,  2]:', '%35s' % x, '%35s' % y, equal(x, y, 1, 2)
        print >>fd, '[1,100]:', '%35s' % x, '%35s' % y, equal(x, y, 1, 100)
    fd.close()

def main():
    'entry point'
    test_c()

if __name__ == '__main__':
    main()

# Run example
# Yes, the error depends on the magnitude.
'''
[1,  2]:                               a - b                            -(b - a) 0.0
[1,100]:                               a - b                            -(b - a) 0.0
[1,  2]:                               a / b                         1 / (b / a) 0.259
[1,100]:                               a / b                         1 / (b / a) 0.257
[1,  2]:                            (a*b)**4                           a**4*b**4 0.754
[1,100]:                            (a*b)**4                           a**4*b**4 0.784
[1,  2]:                          (a + b)**2                 a**2 + 2*a*b + b**2 0.459
[1,100]:                          (a + b)**2                 a**2 + 2*a*b + b**2 0.564
[1,  2]:                     (a + b)*(a - b)                         a**2 - b**2 0.655
[1,100]:                     (a + b)*(a - b)                         a**2 - b**2 0.476
[1,  2]:                          e**(a + b)                           e**a*e**b 0.556
[1,100]:                          e**(a + b)                           e**a*e**b 0.784
[1,  2]:                            ln(a**b)                             b*ln(a) 0.548
[1,100]:                            ln(a**b)                             b*ln(a) 0.292
[1,  2]:                             ln(a*b)                         ln(a)+ln(b) 0.422
[1,100]:                             ln(a*b)                         ln(a)+ln(b) 0.262
[1,  2]:                                 a*b                    e**(ln(a)+ln(b)) 0.332
[1,100]:                                 a*b                    e**(ln(a)+ln(b)) 0.896
[1,  2]:                         1/(1/a+1/b)                       (a*b)/(a + b) 0.495
[1,100]:                         1/(1/a+1/b)                       (a*b)/(a + b) 0.459
[1,  2]:         a*((sin(b))**2+(cos(b))**2)                                   a 0.233
[1,100]:         a*((sin(b))**2+(cos(b))**2)                                   a 0.224
[1,  2]:                         sinh(a + b)     (e**a*e**b - e**(-a)*e**(-b))/2 0.774
[1,100]:                         sinh(a + b)     (e**a*e**b - e**(-a)*e**(-b))/2 0.985
[1,  2]:                          tan(a + b)               sin(a + b)/cos(a + b) 0.323
[1,100]:                          tan(a + b)               sin(a + b)/cos(a + b) 0.319
[1,  2]:                          sin(a + b)         sin(a)*cos(b)+sin(b)*cos(a) 0.655
[1,100]:                          sin(a + b)         sin(a)*cos(b)+sin(b)*cos(a) 0.816
'''
