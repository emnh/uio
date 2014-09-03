#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python ts=4 sw=4 sts=4 et fenc=utf-8
# Original author: "Eivind Magnus Hvidevold" <hvidevold@gmail.com>
# License: GNU GPLv3 at http://www.gnu.org/licenses/gpl.html


def main():
    s = 0
    k = 1
    M = 100

    # First error, k <= M instead of k < M
    while k <= M:
        # Second error, should be float 1.0 instead of 1
        s += 1.0/k

        # Third error, missing increment of k
        k += 1

        print s

if __name__ == '__main__':
    main()

