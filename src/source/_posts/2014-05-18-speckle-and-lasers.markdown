---
layout: post
title: "Speckle and lasers"
date: 2014-05-18 09:26:40 -0500
comments: true
published: true
categories: math optics
---

We know that lasers are very accurate instruments, emit a very precise
wavelength and are in an array of precision applications
including [bloodless surgery][blood], [eye surgery][eye] and 
[fingerprint detection][finger]. That begs a question: 
when we shine a laser on anything,
why do we see bright and dark spots? Shouldn't it all be the same color since
lasers are deterministic (read: not random)?  To
answer that question[^1], we need to delve into optical theory.

<!--More-->

[*Coherent* optical systems][coherence] are simply defined to be
*deterministic* systems. That's a big definition, so let's break it into
pieces. Coherent systems are where you know the wavelength and phase of every
ray. Lasers are very coherent (one wavelength, same phase) while sunlight is
not coherent (many wavelength, different phases).

Deterministic is just a way of saying everything about the system is known and
there's no randomness. Sunlight is not deterministic because there are many
random processes. Photons are randomly generated and there are many
wavelengths. Sunspots are one example of this randomness.

But if lasers are coherent and deterministic, why do we see speckle (read:
bright and dark spots) when we see a laser spot? The speckle is random; we
can't predict where every dark spot will be. The randomness of this laser spot
and the fact that lasers are deterministic throws a helluva question at us. It
turns out *what* we see the laser on is important, but let's look at the math
and physics behind it.

Coherent optical systems have a very special property. Their 
[impulse response][ir] (read: reaction to a small input)
in the frequency domain is just the pupil function.  For those familiar with
the parlance and having $f_x$ be a spatial frequency as opposed to a time
frequency,

$$H\left( f_x, f_y\right) = P(x, y) $$

When I saw this derived, I thought "holy shit." If you just want to only pass high
frequency spatial content (read: edges), then all that's required it to not let
light through the center of the lens.

{% img right https://raw.githubusercontent.com/scottsievert/side-projects/master/speckle/impulse_respone.png 200 %}

Since this system is linear, we can think of our output as bunch of impulse
responses shifted in space and scaled by the corresponding amount. This is the
definition of [convolution][conv] and only works because this is a 
[linear and space invariant system.][LTI]

To find our impulse response in the space domain, $h\left( x, y\right) $, we
have to take the Fourier transform (aka FFT) of our pupil. Since our pupil
function is symmetric, the inverse Fourier transform and forward Fourier
transform [are equivalent][fft].

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

What angles can a wave be thought of as? The frequency content and angles turn
out to be related, since two planes waves of a constant frequency adding
together can have a change in frequency depending on what angle they're at,
which makes intuitive sense. Or, our spatial plane wave $U(x,y)$ can be
represented by the Fourier transform:

$$\textrm{APWS}(x, y) = \mathcal{F}\left\{ U(x,y) \right\}\rvert_{f_x = \theta/\lambda}$$

The wall which the laser is shining on is not smooth and perfectly flat. It's
rough, and the distance adds a phase difference between two waves. Through the
[Drunkard's Walk][rand] and the angular plane wave spectrum, if we could
obtain every angle, the laser spot wouldn't have any speckle. Our eyes are finite in
size, so we can't obtain every angle or frequency.

Because the wall gives the wave some random phase, we can represent the spot we
see by a 2D convolution with a random phase and the impulse response. This
convolution is just saying that every spot gives the same response multiplied
by some random phase, added together for every point.

```python
x = exp(1j*2*pi*rand(N,N)) # a bunch of random phases
x *= p # only within the pupil

d = N/10 # delta since our eyes aren't infinitely big
y = convolve2d(x, h[N/2-d:N/2+d, N/2-d:N/2+d]) # an approximation with d
```

The laser spot `y` shows some speckle! The speckle varies with how large we
make `d` (really `delta` but that's long); if we include more frequencies and
more of the impulse response, the dots get smaller. To see this, if you hold a
pinhole up to your eye, the speckles will appear larger.

{% img center https://raw.githubusercontent.com/scottsievert/side-projects/master/speckle/speckle.png 500 %}

An intuitive way to think about this involves the impulse response. The impulse
response changes on with the distance and so does the phase. Certain areas add
up to 0 while others add up to 1. There's a whole probability density function
that goes with that, but that's goes further into optical and statistical
theory.

**tl;dr:** the roughness of the walls add uncertainty in phase and hence speckle

[^1]:the [full code][code] is available on Github.

[LTI]:https://en.wikipedia.org/wiki/LTI_system_theory
[code]:https://github.com/scottsievert/side-projects/tree/master/speckle
[coherence]:https://en.wikipedia.org/wiki/Coherence_(physics)
[finger]:https://en.wikipedia.org/wiki/Fingerprint
[eye]:https://en.wikipedia.org/wiki/Laser_eye_surgery_(disambiguation)
[blood]:https://en.wikipedia.org/wiki/Bloodless_surgery
[rand]:https://en.wikipedia.org/wiki/Random_walk
[fft]:https://en.wikipedia.org/wiki/Fourier_transform#Invertibility_and_periodicity
[conv]:https://en.wikipedia.org/wiki/Convolution
[ir]:https://en.wikipedia.org/wiki/Impulse_response
