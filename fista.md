
<!--thermal camera blurb-->

It's possible to reconstruct almost any real-world signal from only a few
measurements.

If you're building a single-pixel camera like I am, it sure seems pointless to
move the sensor to location after location sampling nearly the same thing. Math
finds a way around any tricky problem; I sure bet it can find a way around this
one!



<!--image-->

How? To answer that, we need to delve deep into some mathematical theory.

#### Haar Wavelets
The [wavelet transform] is some basic mathematical theory and the [Haar wavelet
transform] is even more basic (but still complex!). The wavelet transform is
very similar to the [Fourier transform] but contains information about time and
(some notion of) frequency.

Essentially, given a signal of length $2^n$ it adds and subtracts nearby
components and places them in the first and last halves of the array
respectively. It recursively goes on until there are only two elements left.
A graph and a small example are shown below.

```python
[1] [2] [3] [4]
[1]+[2] [3]+[4] [1]-[2] [3]-[4]
[1]+[2]+[3]+[4] [1]+[2]-([3]+[4]) [1]-[2] [3]-[4]
```
<!--img-->

If you want more info, there are some useful links out there: [1] [2] [3].

To get the 2D wavelet transform, we just take the wavelet transform of each row
then each column. The important thing is that this matrix is *sparse* in this
wavelet basis.

So what does all of this theory mean in the real world? A nonzero wavelet term
corresponds to an edge. To see this, let's take the inverse transform of 
`[8 0 0 0 0 0 -1 0]`. Because the wavelet transform carries information about
time/space, every one of these indicies correspond to specific set of indices:
the first and second terms correspond to the whole signal, the third and fourth
correspond to the first and last halves and so on. The last term corresponds to
the indices 7 and 8. So, let's see what's at those indices.

The inverse transform is `c[1 1 1 1 1 1 1 0]`. That is, there's an edge
between indices 7 and 8! A non-zero wavelet term corresponds to indices that
contains an edge somewhere.

#### Tree
The 2D Haar Wavelet transform has a nice property: it's tree-structured. That
is, if we know that a parent node is zero then all of it's children must also
be zero. This makes sense with the recursive nature of the wavelet transform;
we can see it for small cases.

Any real-world signal has this tree structure; in essence, bring points don't
lie in dark areas. This makes an important assumption that our resolution is
high enough to capture any edges.

#### Sparsity
As shown above, the wavelet transform for any *real-world* signal is mostly
zeros because the subtraction plays an important role. This signal being mostly
zeros is called [*sparsity.*] It may not seem like much, but it's critical and 
[compressed sensing] relies on this. Powerful inferences can be made sparsity.

#### FISTA
One such powerful inference is that we can reconstruct any sparse vector
through select point samples through the Fast Iterative Soft Thresholding
Algorithm. To me, this is a magic black box that reconstructs a sparse vector
pretty accurately.






We have an input signal, `[1] [2] [3] [4] [5] [6] [7] [8]`. We want to perform
the Haar wavelet transform on this signal. 
