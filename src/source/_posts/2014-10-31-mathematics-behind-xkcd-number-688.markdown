---
layout: post
title: "Mathematics behind XKCD #688"
date: 2014-10-31 09:56:00 -0500
comments: true
categories: math
---

Two months ago, I [implemented] and tried to explain the theory behind [XKCD #688]. I've since taken a course[^course] that has taught me much of the relevant theory, so I would like to devote a blog post to explaining the *applications* -- I won't try to compress two months into a blog post.

<!--More-->

![xkcd comic](http://imgs.xkcd.com/comics/self_description.png)

I'm betting Randall implemented this with a for-loop even though he probably knows the theory. It's what I would also do (and did) -- a for-loop is just too easy.

```python
x = define_source_image()
for i in arange(7):
    x = process_image(x)
```

![animated comic](https://github.com/scottsievert/xkcd-688/raw/master/out.gif)

This is the natural method, but the theory has some interesting applications. While we could see the theory with the image, we can see it more clearly with the [Fibonacci numbers]. The Fibonacci numbers just add up the two previous Fibonacci numbers. These are typically implemented[^code] in the naïve code below. As we're just calling the equivalent of some function in a for loop, this is very similar to the XKCD code.

```python
def fibonacci(k):
    """ calculate the k-th fibonacci number """
    x = array([0, 1, nan]) # first two fibonacci numbers
    for i in arange(k):
        x[2] = x[0] + x[1]
        x[0:2] = x[1:]
    return x[2]
```

Mathematically, it can be represented as $x\_k = x\_{k-1} + x\_{k-2}$ with $x\_0 = 0$ and $x\_1 = 1$. While this is valid, it doesn't reveal the entire theory. Instead, let's choose to represent it with a matrix:

$$
    \begin{bmatrix}
    x_k \\
    x_{k-1} \\
    \end{bmatrix}
    =
    \mathbf{x_k}
    =
    \mathbf{A} \cdot \mathbf{x}_{k-1}
    =
    \begin{bmatrix}
    1 & 1 \\
    1 & 0 \\
    \end{bmatrix}
    \begin{bmatrix}
    x_{k-1} \\
    x_{k-2} \\
    \end{bmatrix}
$$

Calculating the Fibonacci numbers is also an example of [fixed point iteration]. With this method if we wanted to calculate the $k$th Fibonacci number $x\_k$ we'd have do $k$ matrix multiplications. 

$$
    \begin{align*}
    \mathbf{x}_k &= \mathbf{A}\cdot \mathbf{x}_{k-1} \\ 
    &= \mathbf{A}\cdot \left( \mathbf{A}\cdot \mathbf{x}_{k-2} \right) \\
    &= \mathbf{A}\cdot \mathbf{A}\cdot \mathbf{A} \cdots \mathbf{A} \cdot \mathbf{x}_0 \\
    &= \mathbf{A}^k \cdot \mathbf{x}_0
    \end{align*}
$$

We'd just compute $\mathbf{A}^k$ by using [`np.linalg.matrix_power`][matrix_power] to implement this, but naïve [matrix multiplication] is expensive timewise. Calculating $\mathbf{x}\_k$ naïvely has a [computational complexity] of $O(k\cdot n^3)$ when $\mathbf{A}$ is a $n \times n$ matrix. The cost of this algorithm drastically increases with $n$. This could be the number of pixels in our image or the number of locations a GPS records. Powerful algorithms like the FFT with their complexity of $O(n \log n)$ drastically outweigh this seemingly simple Fibonacci calculation.

[matrix_power]:http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.matrix_power.html

For the Fibonacci case, $\mathbf{A}$ remains constant and math has several nice ways[^other] to speed things up. One convenient way is to find a diagonal representation of the matrix called $\mathbb{\Lambda}$ because then we could find $\mathbf{A}^k$ easily. To do that, we'll need to find $\mathbb{\mathbb{\Lambda}}^k$ first. 

[^other]:The current limit for computing $A^k$ is done with the [Coppersmith-Winograd algorithm](http://en.wikipedia.org/wiki/Coppersmith–Winograd_algorithm) with a computation complexity of $O(n^{2.3727}\log k)$.

$$
    \mathbb{\Lambda}^k = 
    \mathbb{\Lambda} \cdot \mathbb{\Lambda} \cdot \ldots \cdot \mathbb{\Lambda} =
     \begin{bmatrix}
       \lambda_{_1}^k    &                &        &                \\
                         & \lambda_{_2}^k &        &                \\
                         &                & \ddots &                \\
                         &                &        & \lambda_{_n}^k \\
     \end{bmatrix}
$$

But we can't just arbitrarily lose information. It turns out that for the right choices[^calculate] of $\mathbf{Q}$ and $\mathbb{\Lambda}$ involving eigenvalues and eigenvectors we get[^limit] $\mathbf{A} = \mathbf{Q} \cdot\mathbb{\Lambda}\cdot \mathbf{Q}^{-1}$. We really want $\mathbf{A}^k$ for our fixed point iteration, and we can get it in terms of $\mathbb{\Lambda}$ and $\mathbf{Q}$ by using the fact that $\mathbf{Q}\cdot\mathbf{Q}^{-1} = \mathbf{I}$ and anything times this identity $\mathbf{I}$ is itself:

$$
    \begin{align*}
    \mathbf{A}^k &= (\mathbf{Q}\cdot \mathbb{\Lambda}\cdot \mathbf{Q}^{-1}) \cdot (\mathbf{Q}\cdot \mathbb{\Lambda}\cdot \mathbf{Q}^{-1}) \cdots (\mathbf{Q}\cdot \mathbb{\Lambda}\cdot \mathbf{Q}^{-1}) \\
    &= \mathbf{Q} \cdot \mathbb{\Lambda}^k\cdot \mathbf{Q}^{-1}
    \end{align*}
$$ 

Because of this added $\mathbf{Q}$ we find that computing $\mathbf{A}^k$ takes $O(n\log n)$ time assuming we're given  $\mathbb{\Lambda}$. Computing $\mathbb{\Lambda}$ requires $O(n^3)$ time meaning that $\mathbf{A}^k$ can be computed in $O(n\log n + n^3) \approx O(n^3)$ time. Over the naïve code for the simple case, this is a large speed up! A factor of $k$ -- which could be as large as a hundred -- is nothing to sneer at!

But... wait. We don't care about every value in the vector this Fibonacci case. We only care about $x\_k$. We already have a [closed form solution] for $\mathbf{x}\_k$ but after doing the matrix multiplication we find that $x\_k$ has a simple formula. With the associated matrices $\mathbf{Q}$ and $\mathbb{\Lambda}$ we find that

$$
x_k = \frac{1}{\sqrt{5}} (\lambda_1^k - \lambda_2^k) = 
\frac{1}{\sqrt{5}} \left[
    \left(\frac{1+\sqrt{5}}{2}\right)^k - \left(\frac{1-\sqrt{5}}{2}\right)^k
\right]
$$

Let's think about what I'm saying here. I'm saying that a formula involving three irrational numbers with two raised to a power is an integer *and* the $k$th Fibonacci number. I mean, even the irrational [golden ratio] $\phi = (1 + \sqrt{5})/2 = 1.618\cdots$ appears! The last thing we would expect is a rational number, much less an integer. But the theory is solid and the first values of $x\_k$ are $0, 1, 1, 2, 3, 5, 8$ -- the Fibonacci numbers!

This means that we can just define our `fibonacci` function to run *fast*. If we want a single value, this algorithm runs in $O(1)$ time vs the naïve code that ran in $O(k)$ time. 

```python
def fibonacci(k):
    """ returns the k-th fibonacci number """
    l_1 = (1 + sqrt(5)) / 2
    l_2 = (1 - sqrt(5)) / 2
    return (l_1**k - l_2**k) / sqrt(5)
```

This theory of eigenvalues and eigenvectors *must* have other insights. Eigenvalues applied themselves well to the Fibonacci problem; where else could they be used? 

The most obvious application is with [stability]. The definition of stability I'll use is that a system (which can be represented by a matrix) is stable if it doesn't blow up towards infinity. Since $\left\|x\_k\right\| \propto \left(\left\|\lambda\right\|\_\max\right)^k$ for large $k$, this system only converges if $ \left\|\lambda \right\|\_\max < 1$ and blows up if $\left\| \lambda \right\|\_\max > 1$. We can see that clearly with our Fibonacci sequence as our largest eigenvalue is the golden ration and greater than one. As expected, the Fibonacci numbers blow up towards infinity.

Can we just glance at a matrix to tell if the corresponding system is stable? This involves complex problems like factoring an $n$th degree polynomial and finding a [determinant]. For the general case, there's no simple easy method besides the computer sitting at your hands with the function `eig` in `numpy.linalg`. Take that with a grain of salt as there might be some relation between eigenvalues and the [z-transform] because a [causal] system only converges if it has poles $\left\|p\right\|$ with $\left\|p\right\| < 1$. This also involves factoring an $n$th degree polynomial but it's a little easier to obtain.

Stability is critical for differential equations, and eigenvalues play a critical role in determining stability for certain differential equations. As you may know, differential equations govern our world. Examples of differential equations are found everywhere -- they govern the size of animal populations and how airplanes fly.

Another more interesting application is with social networks. If you want to see how many friend groups are in some social network, you can just count the eigenvalues that are 0. But there are people I only interact with occasionally; are we in the same friend group? Accordingly, calculating small eigenvalues is much more time intensive.

There are more uses of eigenvalues including machine learning concepts such as principle component analysis and face recognition. One interpretation of eigenvalues is that they're a convenient way of representing a matrix with some very nice properties but I'm betting there's more as it seems that any interesting application involves eigenvalues in some way.

[closed form solution]:https://en.wikipedia.org/wiki/Closed-form_expression
[StackExchange question]:http://math.stackexchange.com/questions/36815/a-simple-explanation-of-eigenvectors-and-eigenvalues-with-big-picture-ideas-of
[determinant]:https://en.wikipedia.org/wiki/Determinant
[causal]:https://en.wikipedia.org/wiki/Causality
[z-transform]:https://en.wikipedia.org/wiki/Z-transform
[stability]:https://en.wikipedia.org/wiki/Linear_stability
[non-contractive map]:https://en.wikipedia.org/wiki/Contraction_mapping
[linear function]:https://en.wikipedia.org/wiki/Linear_function
[fixed point iteration]:https://en.wikipedia.org/wiki/Fixed_point_(mathematics)
[state vector]:https://en.wikipedia.org/wiki/State_space_representation
[mar]:https://en.wikipedia.org/wiki/Markov_chain
[matrix multiplication]:http://en.wikipedia.org/wiki/Matrix_multiplication
[FFT]:https://en.wikipedia.org/wiki/Fast_Fourier_transform
[computational complexity]:https://en.wikipedia.org/wiki/Computational_complexity_theory
[^complex]:But eigenvalues can be complex -- having $\mathbb{\Lambda}=1$ is not nearly the only case where $\|\mathbb{\Lambda}\|=1$.
[Schrödinger equation]:https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation
[Navier-Stokes equation]:https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations
[^theory]:If you need a primer, check out my [previous blog post].
[golden ratio]:https://en.wikipedia.org/wiki/Golden_ratio
[XKCD #688]:http://xkcd.com/688/
[^course]:This course is called Applied Linear Algebra. I covered why this course name sounds basic in a [previous blog post]. This covered the seemingly simple names of dimensions, linear functions and linear algebra and eventually built up to why computers are nesessary.
[previous blog post]:http://scottsievert.github.io/blog/2014/07/31/common-mathematical-misconceptions/
[implemented]:https://github.com/scottsievert/xkcd-688
[^code]:I don't want to clutter up the code so I use `from pylab import *`. Yes it is bad practice... but man it's nice.
[Fibonacci numbers]:http://en.wikipedia.org/wiki/Fibonacci_number
[^limit]:Well, there are certain restrictions, one being $A$ has to have distinct eigenvalues.
[^calculate]:If you want to calculate $Q$ and $\mathbb{\Lambda}$, see the [wiki page](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors). More intuition is present in a [StackExchange question].
[eigenvectors and eigenvalues]:http://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors

