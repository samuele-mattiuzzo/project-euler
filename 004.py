#!/usr/bin/python

import os, sys


def solve():
	print '''
		A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 * 99.
		Find the largest palindrome made from the product of two 3-digit numbers.
	'''

	res = -1
	for c in range(999, 99, -1):
		for z in range(999, c-1, -1):
			t = c * z
			if str(t) == str(t)[::-1]:
				res = t if t > res else res
	return res

def main():
	res = solve()
	print "Solution: %s " % (str(res))

if __name__=="__main__":
	main()
