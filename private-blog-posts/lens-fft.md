
The [Fourier transform][wiki-fourier] or FFT is a powerful mathematical
concept. It breaks an input signal down into it's frequency components. The
best example is lifted from Wikipedia.

{% img right https://upload.wikimedia.org/wikipedia/commons/7/72/Fourier_transform_time_and_frequency_domains_%28small%29.gif 200%}

The Fourier transform is used in almost every type of analysis. I've seen it
used to detect vehicles smuggling contraband crossing borders and to seperate
harmonic overtones from a cello. It can transform [convolution][conv] into a
simple (and fast!) multiplication and multiply incredibly long polynomials.
These might seem pointless, but they're useful with any "[nice][lti]" system
and complicated system stability problems, respectively. The Fourier transform
is perhaps the most useful abstract mathematical concept.

We can see that it's very abstract and mathematical just by looking at it's
definition:

$$ F(f_x) = \fourier{f(x)} = \int f(x) \exp\left[ -j2\pi f_x x \right] dx$$

The Fourier transform is so useful, it's implemented in probably every language
(through `fft`) and there are even dedicated chips to perform this transform
efficiently. The last thing we would expect is for this abstract and
mathematical concept to be implemented by physical devices.

We could easily have some integrated chip perform an FFT, but that's not
interesting. If a physical device that has some completely unrelated purpose
but can still perform an FFT without human intervention (read: programming),
that'd be interesting. For example, an optical lens is shaped solely to produce
an image, not to take a Fourier transform... but that's exactly what it does.

Let me repeat: a *lens can take an exact spatial Fourier transform.* This does
have some limitations[^1], mainly that it only works under coherent light. A
coherent light source is simply defined a source that's not random. Natural
light is random as there are many different wavelengths coming in at random
times. Laser light is very coherent -- there's a very precise wavelength and
every individual ray is in phase[^3].

Goodman, the textbook that almost every Fourier optics course uses, says[^2]
that the field corresponding to the diagram is

$$ 
U_f(u,v) = 
\frac{
    A \exp\left[ j \frac{k}{2f} (1 - d/f) (u^2 + v^2) \right]
                }{j \lambda f}
    \cdot
    \int \int U_o(x,y) \exp\left[ -j \frac{2\pi}{\lambda f} (xu + yv) \right]
    dxdy
$$

When $d=f$, *that's exactly the definition of a Fourier transform.* Meaning we
can expect $U_f(u,v) = \fourier{U_i(x,y)}\big|_{f_x = x/\lambda f} $. Minus
some physical scaling, that's an *exact* Fourier transform.

No matter how elegant this math was, I wanted to see it in the real world. I
decided to use a simple step and compare computer FFT and this lens FFT.

<!--experiment setup-->
<!--computer fft of step-->
<!--laser fft lens of step-->

This alone is cool, but it shows itself elsewhere. The transfer
function is just the pupil function or $$H\left(f_x, f_y\right) = P(x,y) $$
(under coherent light, but has similar effect in incoherent light). If you want
to resolve a higher frequency (aka more detail), you need your pupil function to
extend further.

Animals have different shaped *pupils* or different *pupil functions* for their
eye. A cat has a very vertical pupil, a zebra's pupil is horizontal and an
eagle's pupil is round. There are different evolutionary reasons why an animal
needs to see more detail in the vertical or horizontal directions (ie, jumping
vs hunting) and this shows itself with their pupils.

[^1]:Another limitation: the lens can only accept frequencies so large as
$r/\lambda f$, meaning the input signal must be band-limited.
[^2]:on page ___.
[^3]:For a detailed explanation of why the laser spots we see aren't in phase,
see my [previous blog post][prev-post]

[prev-post]:http://scottsievert.github.io/blog/2014/05/18/speckle-and-lasers/
[wiki-fourier]:https://en.wikipedia.org/wiki/Fourier_transform
[conv]:https://en.wikipedia.org/wiki/Convolution
[lti]:https://en.wikipedia.org/wiki/LTI_system_theory

<!--XXX: check!-->


