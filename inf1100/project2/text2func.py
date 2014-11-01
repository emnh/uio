#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import sys
import re
from math import sin, cos, pi, exp

class StringFunction(object):

    def __init__(self, expr, independent_variables, **kwargs):
        self.expr = expr
        self.independent_variables = independent_variables
        self.constants = kwargs
        lvars = globals()
        lvars.update(kwargs)
        self.f = eval('lambda %s: %s' % (','.join(independent_variables), expr), lvars)

def parse(fstr):
    match = re.match(r'(?P<expr>.*) is a function of (?P<vars>[a-z])( with parameter (?P<constants>.*))?', fstr)
    expr = match.group('expr')
    variables = match.group('vars')
    constants = match.group('constants')
    if constants == None:
        constants = '_=0'
    sf = "StringFunction('%s', %s, %s)" % (expr, "'%s'" % variables, constants)
    print sf
    esf = eval(sf)
    print esf
    return esf

def test():
    strs = '''sin(x) is a function of x
sin(a*y) is a function of y with parameter a=2
sin(a*x-phi) is a function of x with parameter a=3, phi=-pi
exp(-a*x)*cos(w*t) is a function of t with parameter a=1,w=pi,x=2 '''.splitlines()
    for fstr in strs:
        print 'parsing', fstr
        esf = parse(fstr)
        print esf.f(0)

def main():
    'entry point'
    if len(sys.argv) < 1:
        print 'usage: %s <function-expr>|test' % sys.argv[0]
    fstr = sys.argv[1]
    if fstr == 'test':
        test()
        sys.exit(0)
    parse(fstr)

if __name__ == '__main__':
    main()

# Run example
'''
parsing sin(x) is a function of x
StringFunction('sin(x)', 'x', _=0)
<__main__.StringFunction object at 0x7f31f3b99650>
0.0
parsing sin(a*y) is a function of y with parameter a=2
StringFunction('sin(a*y)', 'y', a=2)
<__main__.StringFunction object at 0x7f31f3b99690>
0.0
parsing sin(a*x-phi) is a function of x with parameter a=3, phi=-pi
StringFunction('sin(a*x-phi)', 'x', a=3, phi=-pi)
<__main__.StringFunction object at 0x7f31f3b99650>
1.22464679915e-16
parsing exp(-a*x)*cos(w*t) is a function of t with parameter a=1,w=pi,x=2 
StringFunction('exp(-a*x)*cos(w*t)', 't', a=1,w=pi,x=2 )
<__main__.StringFunction object at 0x7f31f3b99810>
0.135335283237
'''
