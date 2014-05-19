---
layout: post
title: "Speckle and lasers"
date: 2014-05-18 09:26:40 -0500
comments: true
published: false
categories: math, optics
---

We know that lasers are very accurate instruments. We know that they emit a
very precise wavelength and are used in an array of precision applications
including [bloodless surgery][blood], [eye surgery][eye] and 
[fingerprint detection][finger]. That begs a question: 
when we shine a laser on anything,
why do we see bright and dark spots? Shouldn't it all be the same color?  To
answer that question, we need to delve into optical theory.

<!--Impulse response-->
[Coherent optical systems][coherence] are simply defined to be systems where you know the
phase and wavelength of each component. This is very precise light where you
know what's going on at all times. Sunlight is not like this, as photons are
randomly generated in time at many wavelength. 
Pretty much only lasers are coherent, but if coherent, why does speckle (bright
and dark spots) appear?


Coherent optical systems have a very special property. Their 
[impulse response][ir]
in the frequency domain is just the pupil function.  For those familiar with
the parlance and having $f_x$ be a spatial frequency (as opposed to time),

$$H\left( f_x, f_y\right) = P(x, y) $$

When I saw this derived, I thought "holy shit." If you just want to only pass high
frequency spatial content (read: edges), then all that's required it to not let
light through the center of the lens.

{% img right https://raw.githubusercontent.com/scottsievert/side-projects/master/speckle/impulse_respone.png 200 %}

Since this system is linear, we can think of our output as bunch of impulse
responses shifted in space and scaled by the corresponding amount. This is
[convolution][conv] and only works because this is a linear system.

To find our $H\left( f_x, f_y\right) $, we have to take the Fourier transform (aka FFT) of
our pupil. Since our pupil function is symmetric, the inverse Fourier transform
and forward Fourier transform [are equivalent][fft].

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

An intuitive way to think about this involves the impulse response. The impulse
response changes on with the distance and so does the phase. Certain areas add
up to 0 while others add up to 1. There's a whole probability density function
that goes with that, but that's goes further into optical and statistical
theory.

**tl;dr:** the roughness of the walls add uncertainty in phase and hence speckle

*the [full code][code] is available on Github.*

[code]:https://github.com/scottsievert/side-projects/tree/master/speckle
[coherence]:https://en.wikipedia.org/wiki/Coherence_(physics)
[finger]:https://en.wikipedia.org/wiki/Fingerprint
[eye]:https://en.wikipedia.org/wiki/Laser_eye_surgery_(disambiguation)
[blood]:https://en.wikipedia.org/wiki/Bloodless_surgery
[rand]:https://en.wikipedia.org/wiki/Random_walk
[fft]:https://en.wikipedia.org/wiki/Fourier_transform#Invertibility_and_periodicity
[conv]:https://en.wikipedia.org/wiki/Convolution
[ir]:https://en.wikipedia.org/wiki/Impulse_response
