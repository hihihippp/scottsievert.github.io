---
layout: post
title: "Reconstructing sampled signals"
date: 2014-12-20 20:52:16 -0500
comments: true
categories: math signal-processing
published: false
---

<!--TODO: fix candes double dot-->

Your music player gives an analog or *continuous* signal as output. However,
your music player can't store a continuous signal as that would require an
infinite number of bits. How does your music player go between a set of
music *samples* and a continuous signal?

<!--More-->

<img src="{{ root_url }}/images/filters/source.png" />

It's known from the [Nyquist-Shannon sampling theorem] that a [bandlimited]
signal can *exactly* be reconstructed because we sample at least twice the
highest frequency present in the signal. Because we're collecting information
about all the frequencies present in the signal, we can trust signal processing
to take care of the mathematics behind the solution.

I've only recently learned the mathematics behind this and it's not as
complicated as I thought. If we view the signal in frequency domain with the
Fourier transform (via the `fft`), we can see differences in the sampled signal
and continuous signal. From this, we find that there are certain frequency
components we would like to reduce in amplitude.

If we want to perform this reconstruction in real-time we can't completely kill
all the higher components in the signal, but we can come really close. The
[Parks-McClellan algorithm] and the corresponding `scipy.signal.remez` does a
good job of approximating this ideal filter. This means that we can recover the
signal shown below!

<p style="text-align: center;">
<img src="{{ root_url }}/images/filters/fir1.png" width="70%" />
</p>

This signal does have some delay, and that can be seen by looking at the
[impulse response] of our filter. The impulse response cares most about terms
that are $M/2$ terms behind the current sample (there are $M+1$ non-zero terms
in this filter).

<p style="text-align: center;">
<img src="{{ root_url }}/images/filters/filter_coeffs.png" width="70%" />
</p>

The Nyquist-Shannon sampling theorem only describes a [sufficient condition]:
it says nothing about when the Nyquist condition is not met. Sampling at a
lower rate than Nyquist can have extremely large benefits. Sampling at a higher
rate means hardware that operates quicker, greater transmission bandwidth
and more storage space.

In general, recovering a signal after sampling at less than Nyquist rate can't
be done. As typical, if certain assumptions are made about the input signal, it
is possible to obtain an *exact* reconstruction. 

[compressed sensing]:https://en.wikipedia.org/wiki/Compressed_sensing

Back in 2004, [Emmanuel Candes] was working on a medical imaging problem and
trying to recover the image shown below while only sampling along the white
lines. He was expecting a result slightly better than the state of the art at
the time, image shown in the middle image. When he got the exact reconstruction
shown on the right, he didn't believe it. He even called his friend and a
mathematical giant [Terrence Tao] to prove it could not be done.

<figure>
<p style="text-align: center;">
<img src="{{ root_url }}/images/compressed-sensing/original.png" width="70%" />
<figcaption>
<p style="text-align: center; color: #777; font-size: 14px;"> 
(a) the sampled locations, (b) the expected reconstruction, (c) the actual
reconstruction.
</p></figcaption>
</p>
</figure>

How is this possible? This relies on the image being *sparse* in some domain.
It only contains a limited number of frequencies or areas of a similar color.
Many real world signals are like this. For example, images tend to have many
areas of similar color.

Why does sparsity make this exact reconstruction possible? Because sparsity
limits the available solutions to realistic ones. In this case, if every
solution was available it would be possible to select one that changed far too
rapidly. Knowing and making assumptions about the input image is fair and can
have great benefits.

[optimization]:https://en.wikipedia.org/wiki/Mathematical_optimization
[Emmanuel Candes]:http://statweb.stanford.edu/~candes/
[Terrence Tao]:http://en.wikipedia.org/wiki/Terence_Tao

This is just a brief introduction to magic of signal processing. There is a
much more in depth and much clearer article called [Filling in the blanks] by
Wired. These articles tell a much better story than my limited undergraduate
experience can provide! I would strongly recommend reading them.

One of my current undergrad projects was to develop an app that [Jarvis
Haupt] had thought of to show the magic of signal processing. He wanted to show
that a handheld device (read: your iPhone) could do some relatively fancy
signal processing. The sneak peak below shows that the app takes an image
(possibly from your camera roll!), samples it randomly and reconstructs an
approximation!

[Jarvis Haupt]:http://www.ece.umn.edu/~jdhaupt/

When I started this project, I knew none of the theory behind reconstructing
signals and just implemented the Matlab code in C and crafted a user-interface.
Now that I know some of the theory, I'm excited to share!

<!--Check with Jarvis before saying we're going to release app-->
<!--I expect it's okay-->

[Filling in the blanks]:http://www.wired.com/2010/02/ff_algorithm/all/
[sufficient condition]:https://en.wikipedia.org/wiki/Necessity_and_sufficiency
[Parks-McClellan algorithm]:https://en.wikipedia.org/wiki/Parks–McClellan_filter_design_algorithm
[impulse response]:https://en.wikipedia.org/wiki/Impulse_response
[one-to-one]:http://en.wikipedia.org/wiki/Bijection
[bandlimited]:https://en.wikipedia.org/wiki/Bandlimiting
[Nyquist-Shannon sampling theorem]:https://en.wikipedia.org/wiki/Nyquist–Shannon_sampling_theorem
