#!/usr/bin/env python
from math import sqrt, pi, exp
from json import dumps

def f(x):
  m = 0
  s = 2
  ret = 1 / (sqrt(2) * pi * s)
  ret *= exp(-0.5*((x - m) / s)**2)
  return ret

# from http://stackoverflow.com/questions/477486/python-decimal-range-step-value
def drange(start, stop, step):
  x = start
  while x < stop:
    yield x
    x += step

ds = []
for i in drange(-4,4,0.1):
  d = {
      'x': i,
      'y': f(i),
      }
  ds.append(d)
print dumps(ds)

# JSON display at http://jsbin.com/fosapo/2/edit
