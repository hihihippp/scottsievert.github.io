
from __future__ import division
from pylab import *
from time import time
from scipy.misc import lena, imresize
from numpy.random import permutation as randperm
from IST import dwt2_full, idwt2_full
from IPython.parallel import Client
rc = Client()
dview = rc[:]

@dview.remote(block=True)
def app_parallel():
    def f(x):
        appAlrogirthm()
    #dview.map_sync(f, arange(N))
    map(f, arange(N))

N = 5
x_glob = linspace(0, 1, num=N)
start = time()
y = app()
print time() - start
#pool = Pool()


start = time()
y = app_parallel()
print time() - start

#figure()
#imshow(X, interpolation='nearest', cmap='gray')
#colorbar()
#show()

#figure()
#imshow(Xhat, interpolation='nearest', cmap='gray')
#colorbar()
#show()


