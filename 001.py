#!/usr/bin/python

import os, sys

def solve():
	print '''
		Problem 1:
		If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. 
		The sum of these multiples is 23.
		Find the sum of all the multiples of 3 or 5 below 1000.
	'''
	
	MAX = 1000
	SUM = 0

	for elem in [x for x in range(MAX) if (x%3==0 or x%5==0)]:
		SUM += elem
	return SUM


def main():
	res = solve()
	print "Solution: %s " % (str(res))

if __name__=="__main__":
	main()
