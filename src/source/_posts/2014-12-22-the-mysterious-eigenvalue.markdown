---
layout: post
title: "Applying eigenvalues to the Fibonacci problem"
date: 2014-12-22 19:41:26 -0600
comments: true
categories: math eigen
---

The Fibonacci problem is a well known mathematical problem that models
population growth and was conceived in the 1200s. Leonardo of Pisa aka
Fibonacci decided to use a recursive equation: $x\_{n+1} = x\_{n} + x\_{n-1}$
with the seed values $x\_0 = 0$ and $x\_1 = 1$. Implementing this recursive
function is easy:

<!--More-->

```python
def fib(n):
    if n==1: return 0
    if n==2: return 1
    else: return fib(n-1) + fib(n-2)
```

This recursive calling is expensive as it takes a lot of time and a lot of
memory.[^compiler] The cost of this function might not seem worthwhile -- the Fibonacci
numbers are a well studied problem and it seems like there should be a simple
equation. To see the simplicity and surprising elegance behind this, let's
define the Fibonacci numbers in a matrix language[^matrix]

[^matrix]:I'm assuming you have taken a course that deals with matrices.

[^compiler]:Yes, in some languages some compilers are smart enough to get rid of recursion for some functions.

$$
\mathbf{x}_{n} = \begin{bmatrix}
x_{n+1} \\ x_{n}
\end{bmatrix} =
\begin{bmatrix}
1 & 1 \\ 1 & 0
\end{bmatrix} \cdot
\begin{bmatrix}
x_{n} \\ x_{n-1}
\end{bmatrix} = \mathbf{A}\cdot \mathbf{x}_{n-1}
$$

Calling each of those matrices and vectors variables and recognizing the fact
that $\mathbf{x}\_{n-1}$ follows the same formula allows us to write

$$
\begin{align*}
\mathbf{x}_n &= \mathbf{A} \cdot \mathbf{x}_{n-1} \\
&= \mathbf{A} \cdot \mathbf{A} \cdots \mathbf{A} \cdot \mathbf{x}_0 \\
&= \mathbf{A}^n \cdot \mathbf{x}_0
\end{align*}
$$

where we have used $\mathbf{A}^n$ to mean $n$ matrix multiplications.
The corresponding implementation looks something like this:

```python
def fib(n):
    A = asmatrix('1 1; 1 0')
    x_0 = asmatrix('1; 0')
    # n-1 expensive matrix multiplications
    x_n = np.linalg.matrix_power(A, n).dot(x_0) 
    return x_n[0]
```

While this isn't recursive, there's still an $n-1$ unnecessary matrix
multiplications. It turns out that there's a neat mathematical trick to avoid
this. This trick rests on the mysterious and intimidating eigenvalue and
eigenvector. I thought these were mysterious and magical at first but they're
only a convenient way to represent the same data by representing it as a diagonal matrix. Specifically for some matrix $\mathbf{A}$ they obey

$$\mathbf{A}\cdot\mathbf{x} = \lambda \cdot\mathbf{x}$$

for some eigenvalues $\lambda$ and eigenvectors $\mathbf{x}$. This equation is
satisfied for different eigenvalue $\mathbf{x}$ and different eigenvalues
$\lambda$. Through the way matrix multiplication is defined, we can represent
all of these cases. If we stack the eigenvectors into a matrix called
$\mathbf{X}$ and put the eigenvalues into a diagonal matrix $\mathbf{\Lambda}$,
the way matrix multiplication is defined says

$$\mathbf{A}\cdot\mathbf{X} = \mathbf{X}\cdot\mathbf{\Lambda}$$

This rests on the fact that the left multiplied diagonal matrix
$\mathbf{\Lambda}$ just scales each column of $\mathbf{X}$ by $\lambda\_i$.
The column-wise definition of matrix multiplication makes it clear that this is
represents every case where the equation above occurs (for every $\lambda$ and
every $\mathbf{x}$). If the matrix of eigenvectors $\mathbf{X}$ is
invertible[^inv], then

$$\mathbf{A} = \mathbf{X}\cdot\mathbf{\Lambda}\cdot\mathbf{X}^{-1}$$

[^inv]:Conditions: XXX.

And then because a matrix and it's inverse cancel

$$\mathbf{A}^n = \mathbf{X}\cdot\mathbf{\Lambda}^n\cdot\mathbf{X}^{-1}$$

Because $\mathbf{\Lambda}$ is a diagonal matrix, $\mathbf{\Lambda}^n$ is a
simple computation: every element is just raised to the $n$th power. That means
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
two irrational numbers, a division by another irrational number and even
involves the golden ratio phi $\phi \approx 1.618$! However, it gives exactly
the Fibonacci numbers.

This means we can define our function rather simply:

```python
def fib(n):
    eval1 = (1 + sqrt(5))/2 # the golden ratio phi!
    eval2 = (1 - sqrt(5))/2
    # cheap scalar multiplication
    return (eval1**(n-1) - eval2**(n-1)) / sqrt(5)
def fib_approx(n)
    return 1.618034**n / sqrt(5)
```

This is part of the reason why I'm going to grad school for highly mathematical
signal processing. I find these neat theoretical tricks highly interesting and
engaging, especially if they have other practical benefits. I mean, just look
at this blog post. Mathematics can take some expensive recursive equation and
boil it down to a simple formula. I love that process, especially when it has
other practical benefits.
