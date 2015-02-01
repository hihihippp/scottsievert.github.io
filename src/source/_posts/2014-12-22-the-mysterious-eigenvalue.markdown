---
layout: post
title: "Applying eigenvalues to the Fibonacci problem"
date: 2015-1-31 19:41:26 -0600
comments: true
categories: math
---

The [Fibonacci problem] is a well known mathematical problem that models
population growth and was conceived in the 1200s. [Leonardo of Pisa] aka
Fibonacci decided to use a [recursive] equation: $x\_{n} = x\_{n-1} + x\_{n-2}$
with the seed values $x\_0 = 0$ and $x\_1 = 1$. Implementing this recursive
function is straightforward:[^implement]

[recursive]:https://en.wikipedia.org/wiki/Recursion_(computer_science)
[Leonardo of Pisa]:https://en.wikipedia.org/wiki/Fibonacci
[Fibonacci problem]:https://en.wikipedia.org/wiki/Fibonacci_number

<!--More-->

```python
def fib(n):
    if n==0: return 0
    if n==1: return 1
    else: return fib(n-1) + fib(n-2)
```

Since the Fibonacci sequence was conceived to model population growth, it would
seem that there should be a simple equation that grows almost exponentially.
Plus, this recursive calling is expensive both in time and memory.[^compiler].
The cost of this function doesn't seem worthwhile. To see the surprising
formula that we end up with, we need to define our Fibonacci problem in a
matrix language.[^matrix]

[^matrix]:I'm assuming you have taken a course that deals with matrices.
[^compiler]:Yes, in some languages some compilers are smart enough to get rid of recursion for some functions.

$$
\begin{bmatrix}
x_{n} \\ x_{n-1}
\end{bmatrix} =
\mathbf{x}_{n} =
\mathbf{A}\cdot \mathbf{x}_{n-1} =
\begin{bmatrix}
1 & 1 \\ 1 & 0
\end{bmatrix} \cdot
\begin{bmatrix}
x_{n-1} \\ x_{n-2}
\end{bmatrix} 
$$

Calling each of those matrices and vectors variables and recognizing the fact
that $\mathbf{x}\_{n-1}$ follows the same formula as $\mathbf{x}_n$ allows us to write

$$
\begin{align*}
\mathbf{x}_n &= \mathbf{A} \cdot \mathbf{x}_{n-1} \\
&= \mathbf{A} \cdot \mathbf{A} \cdots \mathbf{A} \cdot \mathbf{x}_0 \\
&= \mathbf{A}^n \cdot \mathbf{x}_0
\end{align*}
$$

where we have used $\mathbf{A}^n$ to mean $n$ [matrix multiplications].
The corresponding implementation looks something like this:

[matrix multiplications]:https://en.wikipedia.org/wiki/Matrix_multiplication#Matrix_product_.28two_matrices.29

```python
def fib(n):
    A   = np.asmatrix('1 1; 1 0')
    x_0 = np.asmatrix('1; 0')
    x_n = np.linalg.matrix_power(A, n).dot(x_0)
    return x_n[1]
```

While this isn't recursive, there's still an $n-1$ unnecessary matrix
multiplications. These are expensive time-wise and it seems like there should
be a simple formula involving $n$. As populations grow exponentially, we would
expect this formula to involve scalars raised to the $n$th power. A simple
equation like this could be implemented many times faster than the recursive
implementation!

The trick to do this rests on the mysterious and intimidating 
[eigenvalues and eigenvectors]. These are just a nice way to view the same data but they have a lot of mystery
behind them. Most simply, for a matrix $\mathbf{A}$ they obey the equation

$$\mathbf{A}\cdot\mathbf{x} = \lambda \cdot\mathbf{x}$$

for different eigenvalues $\lambda$ and eigenvectors $\mathbf{x}$. Through the
way matrix multiplication is defined, we can represent all of these cases. This
rests on the fact that the left multiplied diagonal matrix $\mathbf{\Lambda}$
just scales each $\mathbf{x}_i$ by $\lambda\_i$.  The column-wise
definition of matrix multiplication makes it clear that this is represents
every case where the equation above occurs. 

[eigenvalues and eigenvectors]:https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors

$$
\mathbf{A} \cdot
\begin{bmatrix}
\mathbf{x}_1 & \mathbf{x}_2\\
\end{bmatrix}
= 
\begin{bmatrix}
\mathbf{x}_1 & \mathbf{x}_2\\
\end{bmatrix}
\cdot
\begin{bmatrix}
\lambda_{1} & 0\\
0           & \lambda_2
\end{bmatrix}
$$

Or compacting the vectors $\\mathbf{x}\_i$ into a matrix called $\\mathbf{X}$ and
the diagonal matrix of $\\lambda\_i$'s into $\\mathbf{\\Lambda}$, we find that 

$$\mathbf{A}\cdot\mathbf{X} = \mathbf{X}\cdot\mathbf{\Lambda}$$

Because the Fibonacci eigenvector matrix is invertible,[^inv]

$$\mathbf{A} = \mathbf{X}\cdot\mathbf{\Lambda}\cdot\mathbf{X}^{-1}$$

[^inv]:This happens when a matrix is [diagonalizable].
[diagonalizable]:https://en.wikipedia.org/wiki/Diagonalizable_matrix

And then because a matrix and it's inverse cancel

$$\begin{align*}
\mathbf{A}^n &= \mathbf{X}\cdot\mathbf{\Lambda}\cdot\mathbf{X}^{-1}
\cdot\ldots\cdot
\mathbf{X}\cdot\mathbf{\Lambda}\cdot\mathbf{X}^{-1}\\
&= \mathbf{X}\cdot\mathbf{\Lambda}^n\cdot\mathbf{X}^{-1}
\end{align*}$$


$\mathbf{\Lambda}^n$ is a simple computation because $\mathbf{\Lambda}$ is a
diagonal matrix: every element is just raised to the $n$th power. That means
the expensive matrix multiplication only happens twice now. This is a powerful
speed boost and we can calculate the result by substituting for $\mathbf{A}^n$

$$\mathbf{x}_n = \mathbf{X}\cdot \mathbf{\Lambda}^n \cdot \mathbf{X}^{-1}\cdot\mathbf{x}_0$$

For this Fibonacci matrix, we find that 
$\mathbf{\Lambda} = \textrm{diag}\left(\frac{1+\sqrt{5}}{2}, \frac{1-\sqrt{5}}{2}\right)= \textrm{diag}\left(\lambda\_1, \lambda\_2\right)$.
We could define our Fibonacci function to carry out this matrix multiplication,
but these matrices are simple: $\mathbf{\Lambda}$ is diagonal and
$\mathbf{x}_0 = \left[1; 0\right]$.
So, carrying out this fairly simple computation gives

$$x_n = \frac{1}{\sqrt{5}}\left(\lambda_{_1}^n - \lambda_{_2}^n\right) \approx
\frac{1}{\sqrt{5}} \cdot 1.618034^n$$

We would not expect this equation to give an integer. It involves the power of
two irrational numbers, a division by another irrational number and even the
golden ratio phi $\phi \approx 1.618$! However, it gives exactly the Fibonacci
numbers -- you can check yourself!

This means we can define our function rather simply:

```python
def fib(n):
    lambda1 = (1 + sqrt(5))/2
    lambda2 = (1 - sqrt(5))/2
    return (lambda1**n - lambda2**n) / sqrt(5)
def fib_approx(n)
    # for practical range, percent error < 10^-6
    return 1.618034**n / sqrt(5)
```

As one would expect, this implementation is *fast*. We see speedups of roughly
$1000$ for $n=25$, milliseconds vs microseconds. This is almost typical when
mathematics are applied to a seemingly straightforward problem. There are often
large benefits by making the implementation slightly more cryptic!

I've found that mathematics[^math] becomes fascinating, especially in higher
level college courses, and can often yield surprising results. I mean, look at
this blog post. We went from a expensive recursive equation to a simple and
fast equation that only involves scalars. This derivation is one I enjoy and I
especially enjoy the simplicity of the final result. This is part of the reason
why I'm going to grad school for highly mathematical signal processing. Real
world benefits $+$ neat theory $=$ <3.

[systems]:https://en.wikipedia.org/wiki/Linear_system
[^math]:Not math. Courses beyond calculus deserve a different name.

[PageRank]:https://en.wikipedia.org/wiki/PageRank

[^implement]:The complete implementation can be found [on Github](https://github.com/scottsievert/scottsievert.github.io/blob/master/src/source/_posts/2014-fib.py).
