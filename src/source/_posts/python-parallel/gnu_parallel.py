
from __future__ import division
#from pylab import * # be careful on imports!
from numpy import arange
from time import time
import sys


def test_prime(n):
    prime = True
    for i in arange(2, n):
        if n/i % 1 == 0:
            prime = False
    return prime
def generate_list():
    N = 4e3
    for i in arange(N):
        print i

if __name__ == '__main__':
    if sys.argv[1] == 'list':
        generate_list()
    else:
        n = sys.argv[1]
        n = float(n)
        if n%100 == 0: print "======> ", n
        print test_prime(n)

