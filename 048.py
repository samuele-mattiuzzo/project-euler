#!/usr/bin/python

import os, sys

def solve():
    print '''
        Problem 48

        The series, 11 + 22 + 33 + ... + 1010 = 10405071317.
        Find the last ten digits of the series, 11 + 22 + 33 + ... + 10001000.
    '''

    n = 1000
    total = 0

    for x in range(1, n + 1):
        c = 1
        for y in range(1, x + 1):
            c = (c * x) % 10000000000
        total += c

    return total % 10000000000


def main():
    res = solve()
    print "Solution: %s " % (str(res))

if __name__=="__main__":
    main()
