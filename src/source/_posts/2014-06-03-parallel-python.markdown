---
layout: post
title: "Parallel Python"
date: 2014-06-03 23:29:51 -0500
comments: true
categories: 
---
In the scientific community, executing functions in parallel is critical.
Running a function in parallel can mean hours or even days less execution time.

Perhaps the biggest barrier to parallelization is that it can be too
complicated to produce. The core of the scientific community, academia, often
doesn't even use source control meaning that they're unwilling to invest the
time and energy into something without something to roll back to.

We'll take a complicated and time-consuming function, a not-so-smart way to
test if a number is prime. We could use much smarter methods such as a [Sieve
of Eratosthenes][sieve] or even some NumPy. But let's pretend that this is some
much longer and more intensive computation.

[sieve]:https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

```python
def test_prime(n):
    prime = True
    for i in arange(2, n):
        if n/i % 1 == 0:
            prime = False
    return prime

serial = zeros(N)
for i in arange(N):
    serial[i] = test_prime(i)
```

I don't want to add another package to Python's list of parallel toolboxes
(mostly I'm afraid of [competing standards][xkcd]), but let's define
some functions so we can have a parallel function *easily*[^1].
`some_function.parallel([1,2,3])` will execute `some_function` in parallel with
the inputs `[1,2,3]`.

```python
def parallel_attribute(f):
    def easy_parallize(f, sequence):
        from multiprocessing import Pool
        pool = Pool(processes=4)
        result = pool.map(f, sequence)
        cleaned = [x for x in result if not x is None]
        cleaned = asarray(cleaned)
        pool.close()
        pool.join()
        return cleaned
    from functools import partial
    return partial(easy_parallize, f)

test_primes.parallel = parallel_attribute(test_primes)
```

This parallelization is based of [this wonderful Medium article][medium].
Basically, it was relatively easy to develop and works for at least
semi-complex functions that seem prime for the scientific community.

[medium]:https://medium.com/building-things-on-the-internet/40e9b2b36148

Perhaps the biggest question to ask is about the speedup of this code. Like all
complex subjects, the answer is that it depends. If you are only looping over a
small range of inputs, the overhead of creating a parallelized function is too
high.

More importantly, more cores results in more speedup. Small machines, like this
4-core Macbook Air have parallel results that run twice as fast as serial
results. On an 8-core iMac, it's about 4 times as fast.

If you're running code that takes a long time to run and can be run in
parallel, you probably have access to a large supercomputing institute such as
I do. I have access to [MSI][msi], a resource that has supercomputers with up
to XXX cores available. Running this code on those computers, I see parallel
results that run about XXX as fast.

Too often, some promising example is shown that when applied in the real world
fails. To try and combat this, I decided to use a more complicated example,
calculating a [Mandelbrot set][mandel]. This can be natively parallelized using
NumPy, but I decided to simulate some more complex function.

[mandel]:https://en.wikipedia.org/wiki/Mandelbrot_set

Calculating this Mandelbrot set relies on looping over a two-dimensional grid
(that is, without NumPy support). To parallelize this function, I essentially
only looped over one dimension while parallelizing the other dimension.

```python
def mandel_p(x):
    #m = zeros((N,N)) # reducing the dimension since called with `x`
    m = zeros(N); i=-1
    #for x in linspace(-2, 1, num=N): # called with `x`
    j = -1; i += 1
    for y in linspace(-2, 1, num=N):
        j += 1
        #m[j,i] = mandel_pixel(x, y)
        m[j] = mandel_pixel(x, y)

    return m

mandel_p.parallel = parallel_attribute(mandel_p)
parallel = mandel_p.parallel(linspace(-2, 1, num=N))
parallel = parallel.T # dunno why
```

I see similar results with this code: about 2x speedup on my 4-core and about a
4x speedup on the 8-core iMac.

To be complete, here's the complete list of results:

```
| Function   | $N$ | Serial time (s) | Parallel time (s) | serial / parallel |
| :-:        | :-: | :-:             | :-:               | :-:               |
| Serial     |  1  |    1            |     1             |  1                |
|            |  1  |    1            |     1             |  1                |
| Mandlebrot |  1  |    1            |     1             |  1                |
|            |  1  |    1            |     1             |  1                |
```

[^1]:The full source, including function declarations is 
[available on Github][source]


[source]:https://github.com/scottsievert/scottsievert.github.io/blob/master/src/source/_posts/python-parallel/mandlebrot.py
[msi]:https://www.msi.umn.edu
[view]:http://ipython.org/ipython-doc/dev/parallel/parallel_multiengine.html#creating-a-directview-instance
[xkcd]:http://xkcd.com/927/

