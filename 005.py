#!/usr/bin/python

import os, sys

def solve():
    print '''
        Problem 5

		2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
		What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

	'''

	RES = 2520

	while True:
		test = True
		for i in range(1,21):
			if RES%i!=0:
				test = False
				break
		if test == True:
			break
		else:
			test = True
			RES += 1
	return RES

def main():
    res = solve()
    print "Solution: %s " % (str(res))

if __name__=="__main__":
    main()
