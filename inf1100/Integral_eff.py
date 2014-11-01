#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html

'''
'''

import timeit
from math import sin
vec = range(100)

def trapezoidal(f, a, x, n):
    h = (x-a)/float(n)
    I = 0.5*f(a)
    for i in range(1, n):
        I += f(a + i*h)
    I += 0.5*f(x)
    I *= h
    return I

class Integral_eff:
    def __init__(self, f, a, n=100):
        self.f, self.a, self.n = f, float(a), n

    def __call__(self, x):
        if hasattr(x, '__len__'):
            areas = []
            area = 0
            oldx = self.a
            for newx in x:
                newx = float(newx)
                # we divide n by len(x), otherwise it's more accurate but not more efficient
                area += trapezoidal(self.f, oldx, newx, self.n / len(x))
                #area += trapezoidal(self.f, oldx, newx, self.n)
                oldx = newx
                areas.append(area)
            return areas
        x = float(x)
        return trapezoidal(self.f, self.a, x, self.n)

def slow(vec):
    i = Integral_eff(lambda x: x, 0)
    for x in vec:
        i(x)

def fast(vec):
    i = Integral_eff(lambda x: x, 0)
    i(vec)

def main():
    'entry point'
    print 'slow', timeit.timeit('slow(vec)', 'from Integral_eff import slow, vec', number=100)
    print 'fast', timeit.timeit('fast(vec)', 'from Integral_eff import fast, vec', number=100)
    i = Integral_eff(lambda x: x, 0)
    vec2 = i(vec)
    eps = 1.0E-7
    for x, y in [[i(x), i(x) - y < eps] for x, y in zip(vec, vec2)]:
        print x, y

if __name__ == '__main__':
    main()

# Run example
'''
slow 1.08214187622
fast 0.0743038654327
0.0 True
0.5 True
2.0 True
4.5 True
8.0 True
12.5 True
18.0 True
24.5 True
32.0 True
40.5 True
50.0 True
60.5 True
72.0 True
84.5 True
98.0 True
112.5 True
128.0 True
144.5 True
162.0 True
180.5 True
200.0 True
220.5 True
242.0 True
264.5 True
288.0 True
312.5 True
338.0 True
364.5 True
392.0 True
420.5 True
450.0 True
480.5 True
512.0 True
544.5 True
578.0 True
612.5 True
648.0 True
684.5 True
722.0 True
760.5 True
800.0 True
840.5 True
882.0 True
924.5 True
968.0 True
1012.5 True
1058.0 True
1104.5 True
1152.0 True
1200.5 True
1250.0 True
1300.5 True
1352.0 True
1404.5 True
1458.0 True
1512.5 True
1568.0 True
1624.5 True
1682.0 True
1740.5 True
1800.0 True
1860.5 True
1922.0 True
1984.5 True
2048.0 True
2112.5 True
2178.0 True
2244.5 True
2312.0 True
2380.5 True
2450.0 True
2520.5 True
2592.0 True
2664.5 True
2738.0 True
2812.5 True
2888.0 True
2964.5 True
3042.0 True
3120.5 True
3200.0 True
3280.5 True
3362.0 True
3444.5 True
3528.0 True
3612.5 True
3698.0 True
3784.5 True
3872.0 True
3960.5 True
4050.0 True
4140.5 True
4232.0 True
4324.5 True
4418.0 True
4512.5 True
4608.0 True
4704.5 True
4802.0 True
4900.5 True
'''
