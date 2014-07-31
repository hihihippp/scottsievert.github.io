
When I was in high school and even in part of college, when I heard course
names for higher mathematical classes, it seemed as if they were teaching
something simple that I learned back in middle school. I knew that couldn't be
the case, and I would like to share what I've learned.

### N dimensions
Generalizing to N dimensions is often seen as a pointless mathematical
exercise. This gets confused with some language. Space exists in three
dimensions; we just need three elements or a 3 dimensional vector to describe
any point. Because of this, we say we live in three dimensions. So isn't
generalizing to an $N$ dimensions pointless?

Let's go back to vectors. An $N$ dimensional vector is just one with $N$
components.  Thinking about a grid, we need two numbers to describe any point
on that grid, $x$ and $y$. For the four dimensions we live in, we need four:
$x, y, z, t$.

But wait. That's starting to look like a vector. Why can't we define a five
dimensional vector that includes my age or a six dimensional vector that also
includes my year in school? Thinking about this in the real world, we have data
that has N components all the time. Images on my computer have N pixels and my
GPS records N data points. Almost anything *discrete* is an $N$ dimensional
vector.

This pops up all the time in machine learning, image processing and almost
anywhere that uses linear algebra or a computer. All the vectors and matrices
I've seen have $N$ components, a *discrete* number. Computers only have so many
bits meaning they must also be discrete. That means if we want to do anything
fancy with a computer, we need to use linear algebra.

### Linear algebra 
At first glance, linear algebra seems basic. I know that I learned about linear
functions and algebra in 7th grade. In middle school you might have seen
$y=mx+b$. In linear algebra, you might see $y=Ax+b$ where $y, x,$ and $b$ are
vector and $A$ is a matrix.

A matrix is just nothing more than a collection of vectors. For example, if you
have $M$ students with $N$ features (age, weight, GPA, etc), you can collect
them by simply stacking the vectors. In typical mathematical notation, row $i$
refers to the $i$th student and column $j$ refers to the $j$th feature.

We've defined both vectors and matrices, but what about basic operations? How
do we define addition and multiplication? Mathematical history said that
addition worked element-wise, but multiplication is a bit more interesting.

The dot product or matrix multiplication is defined rather simply, but that
doesn't give you any intuition. You can think of matrix multiplication as
linear combinations of the rows and columns, but that still doesn't tell what
matrix multiplication *means.*

Intuitively, we know that we can transform any matrix into any other matrix
because we can arbitrarily choose numbers. But wait, this looks an awful lot
like an arbitrary function.

For example, let's say we have a set of inputs $x = [1 2 3 4]$ and we want to
perform the function $y = f(x) = 2*x + 1$. In matrix notation, we can just do 

$$y = \begin{bmatrix} 2 0 0 0 \\ 0 2 0 0 \\ 0 0 2 0 \\ 0 0 0 2 \end{bmatrix} 
\cdot
\begin{bmatrix} 1 \\ 2 \\ 3 \\ 4 \end{bmatrix}
+
\begin{bmatrix} 1 \\ 1 \\ 1 \\ 1 \end{bmatrix}
$$

With these functions, we can perform even more powerful actions. We can easily
swap elements or perform different actions on different elements. But, it gets
even more powerful. We can find when a matrix or function simply scales a
vector by finding the eigenvalues and eigenvectors or use the inverse to find
$f^{-1}(x)$.

By definition, a matrix multiplication is *linear.*


[eigen]:
[inverse]:

### Linear functions
All this talk of linear algebra seems pointless and airy. We can define a grid
of numbers and certain operations on that grid, but who cares? Well, computers
care. Linear algebra deals with *discrete* algebra and computers only have a
*discrete* number of bits. Linear algebra is how we interact with the world.

Matrices can represent functions. For example, there's some matrix such that
computes the discrete Fourier transform.

Back in middle school, you learned that a linear function was $y=ax + b$. In
the higher level math, a linear function is when $f{ax + by} = a f{x} +
b f{y}$.

By this definition, a linear function is not as simple as it once was. The FFT
is a linear function, as it's well known that $F(x+y) = F(x) + F(y)$.





[dotpr]:
