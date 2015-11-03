#!/usr/bin/python

import os, sys
from math import sqrt

L = 1000

def compute(d):
    p, k, x1, y, sd = 1, 1, 1, 0, sqrt(d)

    while k != 1 or y == 0:
        p = k * (p/k+1) - p
        p = p - int((p - sd)/k) * k

        x = (p*x1 + d*y) / abs(k)
        y = (p*y + x1) / abs(k)
        k = (p*p - d) / k
        x1 = x
    return x


def prime_sieve(n):
    multiples = []
    for i in range(2, n+1):
        if i not in multiples:
            for j in range(i*i, n+1, i):
                multiples.append(j)
    return multiples

def solve():
    print '''
        Problem 66

        https://projecteuler.net/problem=66
    '''

    res = max((compute(d), d) for d in prime_sieve(L))
    return 0


def main():
	res = solve()
	print "Solution: %s " % (str(res))

if __name__=="__main__":
	main()
