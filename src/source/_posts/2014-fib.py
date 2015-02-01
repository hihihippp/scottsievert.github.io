from __future__ import division
from pylab import *

def fib(n):
    if n==0: return 0
    if n==1: return 1
    else: return fib(n-1) + fib(n-2)
def fib_eq(n):
    lambda1 = (1 + sqrt(5))/2
    lambda2 = (1 - sqrt(5))/2
    return (lambda1**n - lambda2**n) / sqrt(5)
def fib_mat(n):
    A = asmatrix('1 1; 1 0')
    x_0 = asmatrix('1; 0')
    x_n = np.linalg.matrix_power(A, n).dot(x_0)
    return x_n[1]
def fib_approx(n):
    return 1.618034**n / sqrt(5)
def approx_error():
    n = arange(1, 1e3)
    e = array([(1 + sqrt(5))/2, (1-sqrt(5))/2])
    l1 = pow(e[0], n)
    l2 = pow(e[1], n)
    fibs = 1 / sqrt(5) * (l1 - l2)

    approx = fib_approx(n)

    figure()
    semilogy(n, abs(approx-fibs) / fibs)
    show()

for f in [fib, fib_eq, fib_mat]:
    print "\n-------------------------"
    for i in arange(5)+1:
        print "%dth fib number: %f" % (i, f(i))

approx_error() # for n=1e3, % error < 10e-6

"""
%timeit fib(100) ==> 
"""
