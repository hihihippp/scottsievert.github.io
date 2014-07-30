

There are many misconceptions about math once you get beyond calculus.

(note: for the remainder of this blog post, I'll use $x$ to indicate
vectors/matrices and $x$ to indicate scalars)

### N dimensions
Generalizing to N dimensions is often seen as a pointless mathematical
exercise. Since I'm writing a blog post about it, you might guess it's not.

Most people assume we live in three dimensions (really four with time *I
think*). But let's go back to vectors. An $N$ dimensional vector is just one with
$N$ components. Thinking about a grid, we need two numbers to describe any
point on that grid, $x$ and $y$. For the four dimensions we live in, we need
four: $x, y, z, t$.

But wait. That's starting to look like a vector. Why can't we define a five
dimensional vector that includes my age?

$$x = [x y z t 22]$$

Thinking about images with $N$ pixels or read $N$ values off a sensor to get an
$N$ dimensional vector.

Let's say we are in charge of a university and have $N$ students that all have
$M$ features (grades, classes, dorm, finical aid, etc). We can think of this as
a $N$ different vectors with $M$ different components, but that's kinda clunky.
Why not condense this into an $N$ by $M$ matrix (or 2D grid of numbers)? Then
the component at $i,j$ would be the $i$th component of the $j$th vector.

### Linear algebra
Linear algebra sounds basic. We were taught linear functions in 7th grade;
they're just $y=ax + b$, right?

Actually, that equation is accurate when we use matrices. But that opens the
door to a whole jungle of matrix math. For example, how do we define
multiplication? It turns out that the definition we use is rather powerful. We
define multiplication as the [dot product][dotpr]. The definition is

[dotpr]:

$$[a_1 a_2; a_3 a_4] * [b_1 b_2; b_3 b_4] = [...]$$

But we can think about it as a [linear combination][lincomb] of the rows or
columns, explained fantastically by [XXX][xxx].

[lincomb]:

There's also other operations, including the [singular value
decomposition][svd] and [eigenvalues and eigenvectors][eigen]. The SVD splits a
matrix into the dot product of three separate matrices with special properties;
$X = U\Sigma V$. Eigenvalues and eigenvectors sound scary but they just see
when $Ax = \lambda x$ is met.

[svd]:
[eigen]:

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
