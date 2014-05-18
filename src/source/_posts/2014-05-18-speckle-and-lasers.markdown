---
layout: post
title: "Speckle and lasers"
date: 2014-05-18 09:26:40 -0500
comments: true
published: false
categories: math, optics
---

<!--Impulse response-->
[Coherent optical systems][coherence] are simply defined to be systems where you know the
phase and wavelength of each component. This is very precise light where you
know what's going on at all times. Sunlight is not like this, as photons are
randomly generated in time. Only lasers are like this, but it would appear that
lasers are not coherent because we see "speckle" or dots when we see a laser.

[coherence]:https://en.wikipedia.org/wiki/Coherence_(physics)

Coherent optical systems have a very special property. Their 
[impulse response][ir]
in the frequency domain is just the pupil function.  For those familiar with
the parlance and having $f_x$ be a spatial frequency (as opposed to time),

$$H\left( f_x, f_y\right) = P(x, y) $$

When I saw this derived, I thought "holy shit." If you just want to only pass high
frequency spatial content (read: edges), then all that's required it to not let
light through the center of the lens.

Since this system is linear, we can think of our output as bunch of impulse
responses shifted in space and scaled by the corresponding amount. This is
[convolution][conv] and only works because this is a linear system.

[conv]:https://en.wikipedia.org/wiki/Convolution
[ir]:https://en.wikipedia.org/wiki/Impulse_response

To find our $H\left( f_x, f_y\right) $, we have to take the Fourier transform (aka FFT) of
our pupil. Since our pupil function is symmetric, the inverse Fourier transform
and forward Fourier transform [are equivalent][fft].

[fft]:https://en.wikipedia.org/wiki/Fourier_transform#Invertibility_and_periodicity


```python
# a circular pupil
pupil = zeros((N,N))
i = argwhere(x**2 + y**2 < r**2)
pupil[i[:,0], i[:,1]] = 1

h = fft2(pupil) # our impulse response since H(fx) = P(x)
h = fftshift(h)
```

<!--plane wave spectrum-->
Through the angular plane wave spectrum, this impulse response can be viewed as
a series plane waves coming in at different angles, shown in the figure below.

{% img right https://raw.githubusercontent.com/scottsievert/side-projects/master/speckle/apws.png 200 %}

{% img right https://raw.githubusercontent.com/scottsievert/side-projects/master/speckle/impulse_respone.png 200 %}


What angles can a wave be though of as? The frequency content and angles turn
out to be related, since two planes waves of a constant frequency adding
together can have a change in frequency depending on what angle they're at. Or,
our spatial plane wave $U(x,y)$ can be represented by the Fourier transform:

$$U(x, y) = \mathcal{F}\left\{ U(x,y) \right\}\rvert_{f_x = \theta/\lambda}$$

The wall (which the laser is shining on) is not smooth and perfectly flat. It's
rough, and the distance adds a phase difference between two waves. Through the
[random walk processes][rand] and the angular wave spectrum, if we could
obtain every angle, the laser wouldn't have any speckle. Our eyes don't have
infinite dimension, so we can't do that.

[rand]:https://en.wikipedia.org/wiki/Random_walk

Since the impulse response of our impulse response extends out a ways in the
spatial domain and our eyes can't aren't infinitely big, we can't receive the
complete laser image. If our eyes were infinitely large and able to receive the
full impulse response, we wouldn't see any speckle in laser images.

We can model this optical system with a 2D convolution and a bunch of random
phase vectors.

```python
x = exp(1j*2*pi*rand(N,N)) # a bunch of random phases
x *= p # only within the pupil

d = N/2 # delta since our eyes aren't infinitely big
y = convolve2d(x, h[N/2-d:N/2+d, N/2-d:N/2+d])
```

Then the laser shows speckle! This varies on how much of the impulse response
we include; if we include more frequencies, the dots get smaller. This means
that if you hold a pinhole up to your eye, the speckles will appear larger.

{% img center https://raw.githubusercontent.com/scottsievert/side-projects/master/speckle/speckle.png 500 %}



**tl;dr:** the roughness of the walls add uncertainty in phase and hence speckle

The [full code][code] is available on Github.

[code]:https://github.com/scottsievert/side-projects/tree/master/speckle
