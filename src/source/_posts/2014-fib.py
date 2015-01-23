
from __future__ import division
from pylab import *

def fib(k):
    assert(k > 0)
    if k==1: return 0
    if k==2: return 1
    else: return fib(k-1) + fib(k-2)
def fibonacci_for(k):
    x = array([0, 1, nan])
    for i in arange(k-1):
        x[2] = x[0] + x[1]
        x[0], x[1] = x[1], x[2]
    return x[0]
def fib_eq(k):
    l1 = (1 + sqrt(5))/2
    l2 = (1 - sqrt(5))/2
    return (pow(l1, k-1) - pow(l2, k-1)) / sqrt(5)
def fib_mat(k):
    A = asmatrix('1 1; 1 0')
    x_0 = asmatrix('1; 0')
    x_n = pow(A, k-1).dot(x_0)
    return x_n[1]

print "--------------------------------"
for i in arange(5)+1:
    print "%dth fib number: %d" % (i, fibonacci_for(i))
print "--------------------------------"
for i in arange(5)+1:
    print "%dth fib number: %d" % (i, fib(i))
print "--------------------------------"
for i in arange(5)+1:
    print "%dth fib number: %f" % (i, fib_eq(i))
print "--------------------------------"
for i in arange(5)+1:
    print "%dth fib number: %f" % (i, fib_mat(i))

n = arange(1, 100)
e = array([(1 + sqrt(5))/2, (1-sqrt(5))/2])
l1 = pow(e[0], n)
l2 = pow(e[1], n)
fibs = 1 / sqrt(5) * (l1 - l2)

approx = 1 / sqrt(5) * 1.618034**n

semilogy(n, (approx - fibs) / 1)
grid()
show()
