---
layout: post
title: "Common mathematical misconceptions"
date: 2014-07-31 21:12:26 -0500
comments: true
categories: math
---

When I heard course names for higher mathematical classes during high school
and even part of college, it seemed as if they were teaching something simple
that I learned back in middle school. I knew that couldn't be the case, and
three years of college have taught me otherwise.

<!--More-->

## N dimensions
Generalizing to $N$ [dimensions] is often seen as a pointless mathematical
exercise because of a language confusion. Space exists in three dimensions; we
just need three elements or a three dimensional vector to describe any point.
Because of this, we say we live in three dimensions. So isn't generalizing to
an $N$ dimensions pointless?

[dimensions]:https://en.wikipedia.org/wiki/Dimension_(mathematics_and_physics)

Let's go back to [vectors]. An $N$ dimensional vector is just one with $N$
components.[^numpy] Thinking about a grid or 2D graph, we need two numbers to
describe any point on that grid, $x$ and $y$. That's a two dimensional vector.
For the four dimensions we live in, we need four: $x, y, z, t$.

[vectors]:https://en.wikipedia.org/wiki/Vector_space
[^numpy]:And hence an ndarray or "N dimensional array" in NumPy

But wait. Why can't we define a five dimensional vector that includes my age or
a six dimensional vector that also includes my year in school? Thinking about
this in the real world, we have data that has $N$ components all the time. Images
on my computer have $N$ pixels and my GPS records $N$ locations. Almost anything
*discrete* is an $N$ dimensional vector.

This pops up all the time in image processing, machine learning and almost
anywhere that uses linear algebra *or a computer.* All the vectors and matrices
I've seen have $N$ components, a *discrete* number. Computers only have a
finite number of bits[^computer] meaning computers must also be discrete. That
means if we want to do anything fancy with a computer, we need to use linear
algebra.

[^computer]:When computers can have an [uncountably infinite] number of bits they can be continuous and I'll eat my hat

## Linear algebra 
At first glance, [linear algebra] seems like middle school material. In
middle school you might have seen $y=m\cdot x+b$ (more on this linear function
later). In linear algebra, you might see $\mathbf{y}=\mathbf{A\cdot x+b}$ where $\mathbf{y, x,}$ and $\mathbf{b}$ are
vectors and $\mathbf{A}$ is a matrix.[^font]

[^font]:For the rest of this post, I'll use that bold mathematical notation to describe vector and the regular font to describe scalars

[linear algebra]:https://en.wikipedia.org/wiki/Linear_algebra

A matrix is just nothing more than a collection of vectors and 2D grid of
numbers. For example, if you have $M$ students with $N$ features (age, weight,
GPA, etc), you can collect them by simply stacking the vectors and make an
$M\times N$ matrix.

We've defined both vectors and matrices, but what about basic operations? How
do we define addition and multiplication? Addition works element-wise, but
multiplication is a bit more interesting.

[Matrix multiplication] is defined rather simply, but that doesn't give you any
intuition. You can think of matrix multiplication as linear combinations of the
rows and columns, but that still doesn't tell what matrix multiplication
*means.*

Intuitively, we know that we can transform any matrix into any other matrix
because we can arbitrarily choose numbers. But wait. In middle school we
learned that a function could transform any number into any other number.
Matrices are then analogous to functions!

For example, let's say we have a set of inputs $\mathbf{x} = [1,~2,~3,~4]^T$ and we want to
perform the function $y = f(x) = 2\cdot x + 1$ on each element in our vector. In
matrix notation, we can just do 

$$
\mathbf{y} = 
\begin{bmatrix} 2&0&0&0 \\ 0&2&0&0 \\ 0&0&2&0 \\ 0&0&0&2 \end{bmatrix} 
\cdot
\begin{bmatrix} 1 \\ 2 \\ 3 \\ 4 \end{bmatrix}
+
\begin{bmatrix} 1 \\ 1 \\ 1 \\ 1 \end{bmatrix}
$$

With these functions, we can perform even more powerful actions. We can easily
swap elements or perform different actions on different elements. It gets even
more powerful but still relatively simple to an experienced mathematician. We
can find when a matrix or function simply scales a vector by finding the
[eigenvalues and eigenvectors][eigen] or use the [inverse] to find a discrete
analog to $f^{-1}(x)$.

[eigen]:https://en.wikipedia.org/wiki/Eigenvalue
[inverse]:https://en.wikipedia.org/wiki/Inverse_matrix

## Linear functions
A [linear function] seems like the most boring function. It's just a straight
line, right? It is, but English got confused and it also means when some
function obeys the [superposition principle][super]. Concisely in math, it's
when $f(\alpha x+\beta y)=\alpha\cdot f(x)+\beta\cdot f(y)$.

[linear function]:https://en.wikipedia.org/wiki/Linear_function
[super]:https://en.wikipedia.org/wiki/Superposition_principle

This means that *a general linear function is not linear.* If $f(x) = mx+b$,
$f(x+y) = f(x)+f(y)-b$ which doesn't satisfy the definition of a linear
function. But there's much more interesting functions out there.  [Integration]
and [differentiation] respect scalar multiplication and addition, meaning
they're linear.

[Integration]:https://en.wikipedia.org/wiki/Integral
[differentiation]:https://en.wikipedia.org/wiki/Derivative

Since a host of other functions depend on integration and differentiation, so
many of these  functions (but not all!) are also linear.[^linear] The 
[discrete Fourier transform] (computed by `fft`), [wavelet transform] and a host of other
functions are linear.

[discrete Fourier transform]:https://en.wikipedia.org/wiki/Discrete_Fourier_transform
[wavelet transform]:https://en.wikipedia.org/wiki/Wavelet_transform
[^linear]:That is if they only depend on the simplest forms of integration and differentiation

Addition and scalar multiplication are defined element-wise for matrices, so
any linear function can be represented by a matrix. There are matrices for
computing the `fft` and wavelet transform. While unused as they require
$O(n^2)$ operations, they exist. Exploiting specific properties, mathematicians
are often able to push the number of operations down to $O(n\log(n))$.

Linear functions are perceived as boring. If you know $\mathbf{y}$ in $\mathbf{y=Ax}$ for
some known[^mat_comp] matrix $\mathbf{A}$, you can easily find $\mathbf{x}$ by left-multipying
with $\mathbf{A}^{-1}$. This might be expensive time-wise, but an exact solution is
computable.  

Nonlinear functions have a unique property that an exact and closed form
solution [often can't be found][exact]. This means that no combination of
elementary function like $\sin(\cdot), \exp(\cdot), \sqrt{\cdot},\int \cdot~dx,
\frac{d~\cdot}{dx}$ along with respective operators and the infinitely many
real numbers can describe *every* solution.[^solution] Instead, those elementary
functions can only describe the equation that needs to be solved.

[^solution]:It should be noted that *occaisonally* a closed form solution can be found *assuming* certain conditions apply

[^uncount]:The real numbers are actually [uncountably infinite]

[uncountably infinite]:(https://en.wikipedia.org/wiki/Uncountable_set)

Even a "simple" problem such as 
[describing the motion of a pendulum][pend] 
is nonlinear and an exact solution can't be found, even for the most simple
case. Getting even more complex,
there's a whole list of 
[nonlinear parital differential equations][npde] 
that solve important problems.[^head]

[^head]:And these problems are wayyy over my head

[^mat_comp]:And matrix completion handles when $A$ isn't known. This is analgous to finding an unknown scalar function

This is why simulation is such a big deal. No closed form solution can be found
meaning that you have to find a solution numerically.  Supercomputers don't
exist to for mild speed boosts or storage requirements that machine
learning or "big data"[^buzz] seems to require. No, supercomputers exist
because with a nonlinear problem, a simulation *has* to be run to get *any*
result. Running one of these simulations on my personal computer would take
years if not decades.

[^buzz]:Yeah it's a buzz word. For example, satellites that collect 2 billion measurements a day. That's a lot of data, but analyzing it and using it is not "big data."

When you hand this type of problem to an experienced mathematician, they won't
look for a solution. Instead, they'll look for bounds and guarantees on a
solution they work out. If they just came up with a solution, they wouldn't
even know how good it is! So, they'll try to bound the error and look for ways
to lower that error.

When I started college, I was under the impression that my later career would
involve long and messy exact solutions. In my second and third years, I came to
realize that those messy solutions didn't exist and instead we used extremely
elegant math to find exact solutions. In the last couple months[^nonlinear], I have come to
realize that while simple math might *describe* the problem, there's no closed
form solution and the only way to get a solution to "interesting" problems is
with a computer.

[^nonlinear]:Or even as I write this blog post. I've known this for a while but this is a new light

## 

[npde]:https://en.wikipedia.org/wiki/List_of_nonlinear_partial_differential_equations
[exact]:https://en.wikipedia.org/wiki/List_of_nonlinear_partial_differential_equations#Exact_solutions
[pend]:https://en.wikipedia.org/wiki/Pendulum_(mathematics)
[Matrix multiplication]:https://en.wikipedia.org/wiki/Matrix_multiplication

