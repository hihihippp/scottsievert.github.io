
from __future__ import division
from pylab import *

def mills_cross():
    N = 1024
    X = zeros((N,N))

    r_small = 0.5
    r_big = 0.6
    i = linspace(-1, 1, num=N)
    x, y = meshgrid(i,i)
    i = argwhere(pow(x,2) + pow(y,2) < pow(r_big,2))
    j = argwhere(pow(x,2) + pow(y,2) < pow(r_small,2))

    X[i[:,0], i[:,1]] = 1
    X[j[:,0], j[:,1]] = 0

    i = argwhere((abs(x) < 0.03) & (abs(y)<0.2))
    X[i[:,0], i[:,1]] = 1

    j = argwhere((abs(x) < 0.2) & (abs(y)<0.03))
    X[j[:,0], j[:,1]] = 1

    FX = fft2(X)
    FX = fftshift(FX)


    figure()
    imshow(X)
    show()

    figure()
    M = 20
    imshow(abs(FX)[N/2-M:N/2+M, N/2-M:N/2+M])
    show()

def doubleSlit():
    N = 2**10

    X = zeros((N,N))

    X[475:500, 400:500] = 1
    X[575:600, 400:500] = 1

    FX = fft2(X)
    FX = fftshift(FX)

    figure()
    imshow(X)
    show()

    figure()
    M = N/3
    imshow(abs(FX)[N/2-M:N/2+M, N/2-M:N/2+M])
    show()

from scipy.signal import convolve2d as conv
#def grid():
N = 1024
grid = zeros((N,N))

grid[0:10, 0:10] = 1

N_squares = 40
W_squares = 20
starts = arange(0, W_squares, 1.0)
starts *= N / W_squares

for i in starts:
    for j in starts:
        grid[i:i+W_squares,j:j+W_squares] = 1

G = fft2(grid)
G = fftshift(G)
G /= G.max()

wider = ones((4,4))
G = conv(G, wider)

figure()

subplot(1, 2, 1)
imshow(grid)
axis('off')
title('\\textrm{Grid}')

subplot(1, 2, 2)
M = N/10
imshow(abs(G)[N/2-M:N/2+M, N/2-M:N/2+M], interpolation='nearest')
title('\\textrm{Fourier transform}')

axis('off')

savefig('grid.png', dpi=300, bbox_inches='tight', pad_inches=0)
show()
