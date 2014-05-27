
from __future__ import division
from pylab import *

figure()
subplot(3, 1, 1)
imshow(imread('cat.jpg'))
axis('off')

subplot(3, 1, 2)
imshow(imread('eagle.jpg'))
axis('off')

subplot(3, 1, 3)
imshow(imread('zebra.jpg'))
axis('off')

savefig('stack.png', dpi=300, bbox_inches='tight', pad_inches=0)
show()
