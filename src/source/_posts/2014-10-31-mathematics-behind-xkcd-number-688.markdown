---
layout: post
title: "Mathematics behind XKCD #688"
date: 2014-10-31 09:56:00 -0500
comments: true
categories: math
---

What mathematics go behind the [XKCD #688]? In the past two months, I have learned a lot of the theory behind it, much more than I knew when I [implemented] it myself. But I don't want to cover two months of Applied Linear Algebra[^course] so I'll just touch on a couple of the applications.

[^course]:I covered why this course name sounds basic in a [previous blog post]. This covered the seemingly simple names of dimensions, linear functions and linear algebra and eventually built up to why computers are nesessary.

[previous blog post]:http://scottsievert.github.io/blog/2014/07/31/common-mathematical-misconceptions/

<!--More-->

[XKCD #688]:http://xkcd.com/688/

![xkcd comic](http://imgs.xkcd.com/comics/self_description.png)

Randall probably probably just called a function in a for loop (like I would certainly do!).

```python
x = define_source_image()
for i in arange(7):
    x = process_image(x)
```

![animated comic](https://github.com/scottsievert/xkcd-688/raw/master/out.gif)

This is the natural method, but the theory has some interesting applications. While we could see the theory with the image, we can see it more clearly with the [Fibonacci numbers]. The Fibonacci numbers just add up the two previous Fibonacci numbers. These are typically implemented in the naïve code below[^code]:

[implemented]:https://github.com/scottsievert/xkcd-688

[^code]:I don't want to clutter up the code so I use `from pylab import *`. Yes it is bad practice... but man it's nice.
[Fibonacci numbers]:http://en.wikipedia.org/wiki/Fibonacci_number

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

This naïve implemention of this code can calculate our full [state vector] $\mathbf{x}_k$ which can be useful for other similar concepts such as [Markov chains][mar] where $\mathbf{A}$ changes over time. To implement this, we'd just call `x = A.dot(x)` in a for-loop with possible additional processing.

[linear function]:https://en.wikipedia.org/wiki/Linear_function
[fixed point iteration]:https://en.wikipedia.org/wiki/Fixed_point_(mathematics)
[state vector]:https://en.wikipedia.org/wiki/State_space_representation
[mar]:https://en.wikipedia.org/wiki/Markov_chain

This [matrix multiplication] is expensive timewise. Calculating $\mathbf{x}\_k$ via this method has a [computational complexity] of $O(k\cdot n^3)$ when $\mathbf{A}$ is a $n \times n$ matrix. The cost of this algorithm drastically increases with $n$. This could be the number of pixels in our image or the number of locations a GPS records. Powerful algorithms like the FFT with their complexity of $O(n \log n)$ drastically outweigh this seemingly simple Fibonacci calculation.

[computational complexity]:https://en.wikipedia.org/wiki/Computational_complexity_theory

For the Fibonacci case, $\mathbf{A}$ remains constant and math has a nice way to speed things up. One convenient way is to find a diagonal representation of the matrix called $\mathbb{\Lambda}$ because then we could find $\mathbf{A}^k$ easily. To do that, we'll need to find $\mathbb{\mathbb{\Lambda}}^k$ first which only requires $O(k\cdot n)$ operations. We're just doing $k$ multiplications $n$ times as shown below:

[matrix multiplication]:http://en.wikipedia.org/wiki/Matrix_multiplication
[FFT]:https://en.wikipedia.org/wiki/Fast_Fourier_transform

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

But we can't just arbitrarily loose information. It turns out that for the right choices[^calculate] of $\mathbf{Q}$ and $\mathbb{\Lambda}$ involving eigenvales and eigenvectors we get[^limit] $\mathbf{A} = \mathbf{Q} \cdot\mathbb{\Lambda}\cdot \mathbf{Q}^{-1}$. We really want $\mathbf{A}^k$ for our fixed point iteration, and we can get it in terms of $\mathbb{\Lambda}$ and $\mathbf{Q}$ by using the fact that $\mathbf{Q}\cdot\mathbf{Q}^{-1} = \mathbf{I}$ and anything times this identity is itself:

$$
\begin{align*}
\mathbf{A}^k &= (\mathbf{Q}\cdot \mathbb{\Lambda}\cdot \mathbf{Q}^{-1}) \cdot (\mathbf{Q}\cdot \mathbb{\Lambda}\cdot \mathbf{Q}^{-1}) \cdots (\mathbf{Q}\cdot \mathbb{\Lambda}\cdot \mathbf{Q}^{-1}) \\
&= \mathbf{Q} \cdot \mathbb{\Lambda}^k\cdot \mathbf{Q}^{-1}
\end{align*}
$$ 

Because of this added $\mathbf{Q}$ we find that our computational complexity is $O(k\cdot n^2 + n^3)$ for an $n \times n$ matrix. Over the naïve code for the simple case, this is a large speed up! A factor of $k$ -- which could be as large as a hundred -- is nothing to sneer at!

[^limit]:Well, there are certain restrictions, one being $A$ has to have distinct eigenvalues.
[^calculate]:If you want to calculate $Q$ and $\mathbb{\Lambda}$, see the [wiki page](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors). More intuition is present in a [StackExchange question].
[eigenvectors and eigenvalues]:http://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors

But... wait. This $\mathbf{A}^k$ is simple. There's no complicated dot product, only some scalar powers of $\lambda^k$ and constants. While we had a [closed form solution] beforehand for our Fibonacci matrix, this one is *simple*. With the associated $\mathbf{Q}$ and $\mathbb{\Lambda}$ with entiries $\lambda\_1$ and $\lambda\_2$ we find that

$$
x_k = \frac{1}{\sqrt{5}} (\lambda_1^k - \lambda_2^k) = 
\frac{1}{\sqrt{5}} \left[
    \left(\frac{1+\sqrt{5}}{2}\right)^k - \left(\frac{1-\sqrt{5}}{2}\right)^k
\right]
$$

Let's think about what I'm saying here. I'm saying that a formula involving three irrational numbers with two raised to a power is an integer *and* the $k$th Fibonacci number. I mean, even the irrational [golden ratio] $\phi = (1 + \sqrt{5})/2 = 1.618\cdots$ appears! The last thing we would expect is a rational number, much less an integer. But the theory is solid and the first values of $x\_k$ are $0, 1, 1, 2, 3, 5, 8$ -- the Fibonacci numbers!

[golden ratio]:https://en.wikipedia.org/wiki/Golden_ratio

This means that we can just define our `fibonacci` function to run *fast*. If we want a single value, this algorithm runs in almost $O(1)$ time vs the naïve code that ran in $O(k)$ time. Likewise, the matrix multiplication of $\mathbf{Q} \cdot \mathbf{A}\cdot \mathbf{Q^{-1}}$ just results in terms that only have scalar multiplication.

```python
def fibonacci(k):
    """ returns the k-th fibonacci number """
    l_1 = (1 + sqrt(5)) / 2
    l_2 = (1 - sqrt(5)) / 2
    return (l_1**k - l_2**k) / sqrt(5)
```

This theory of eigenvalues and eigenvectors *must* have other insights. The most obvious one is [stability]. The definition of stability I'll use is that a system (which can be represented by a matrix) is stable if it doesn't blow up towards infinity. Since $\left\|x\_k\right\| \propto \left(\left\|\lambda\right\|\_\max\right)^k$ for large $k$, this system only converges if $ \left\|\lambda \right\|\_\max < 1$ and blows up if $\left\| \lambda \right\|\_\max > 1$. We can see that clearly with our Fibonacci sequence as our largest eigenvalue is the golden ration and greater than one. As expected, the Fibonacci numbers blow up towards infinity.

Can we tell by looking if any system represented by a matrix is stable? This complex problems like factoring an $n$th degree polynomial and finding a [determinant]. There's no simple easy method besides the computer sitting at your hands with the function `eig` in `numpy.linalg`. Take that with a grain of salt as there might be some relation between eigenvalues and the [z-transform] because a [causal] system only converges if it has poles $\left\|p\right\|$ with $\left\|p\right\| < 1$. This also involves factoring an $n$th degree polynomial but it's a little easier to obtain.

[determinant]:https://en.wikipedia.org/wiki/Determinant
[causal]:https://en.wikipedia.org/wiki/Causality
[z-transform]:https://en.wikipedia.org/wiki/Z-transform
[stability]:https://en.wikipedia.org/wiki/Linear_stability
[non-contractive map]:https://en.wikipedia.org/wiki/Contraction_mapping

[^complex]:But eigenvalues can be complex -- having $\mathbb{\Lambda}=1$ is not nearly the only case where $\|\mathbb{\Lambda}\|=1$.

Stability is critical for differential equations, and eigenvalues play a critical role in determining stability for certain differential equations. As you may know, differential equations are functions that govern our world. There are many examples but the unsolved [Navier-Stokes equation] governs fluid flow and the [Schrödinger equation] governs quantum mechanics.

[Schrödinger equation]:https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation
[Navier-Stokes equation]:https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations

Another more interesting application is with social networks. If you want to see how many friend groups are in some social network, you can just count the eigenvalues that are 0. But there are people I only see sometimes; are we in the same friend group? Accordingly, calculating smaller eigenvalues is much more time intensive.

There are more uses of eigenvalues including machine learning concepts such as principle component analysis and face recognition. One interpretation of eigenvalues is that they're a convenient way of representing a matrix with some very nice properties but I'm betting there's more. I've talked with signal processors that say it seems like everything rests on eigenvalues.

[closed form solution]:https://en.wikipedia.org/wiki/Closed-form_expression
[StackExchange question]:http://math.stackexchange.com/questions/36815/a-simple-explanation-of-eigenvectors-and-eigenvalues-with-big-picture-ideas-of

[^theory]:If you need a primer, check out my [previous blog post].

