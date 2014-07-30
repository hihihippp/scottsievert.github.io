---
layout: post
title: "Parallel Python"
date: 2014-06-03 23:29:51 -0500
comments: true
categories: python
---

In the scientific community, executing functions in parallel can mean hours or
even days less execution time.  There's a whole array of 
[Python parallelization toolkits][parallel], probably partially due to the 
[competing standards][xkcd] issue.

<!--More-->

Perhaps the biggest barrier to parallelization is that it can be very
complicated to include, at least for the part of the scientific community I'm
in. I spent a while looking at the [IPython parallization framework][ipy] and
various other packages, but they all gave me mysterious bugs so I decided to
use the [multiprocessing library][multi] for this simple task. Without 
[this Medium article][medium], I would be lost in threads and classes that add
significant speed boots but seem to be default in basic parallelization
libraries.

There are *extremely* large speed gains through these other toolboxes. The GPU
has thousands of cores, while your CPU only uses a few. Of course, an easy and
simple solution uses the least complex methods, meaning this simple
parallelization uses the CPU. There are massive gains for using more complex
solutions.

I don't want to add another package to Python's list of parallel toolboxes
(again, [competing standards][xkcd]), but let's define
some functions[^1] so we can have a parallel function *easily*.
`some_function.parallel([1,2,3])` will execute `some_function` in parallel with
the inputs `[1,2,3]`.

```python
def parallel_function(f):
    def easy_parallize(f, sequence):
        """ assumes f takes sequence as input, easy w/ Python's scope """
        from multiprocessing import Pool
        pool = Pool(processes=4) # depends on available cores
        result = pool.map(f, sequence) # for i in sequence: result[i] = f(i)
        cleaned = [x for x in result if not x is None] # getting results
        cleaned = asarray(cleaned)
        pool.close() # not optimal! but easy
        pool.join()
        return cleaned
    from functools import partial
    return partial(easy_parallize, f)

function.parallel = parallel_function(test_primes)
```

The function `easy_parallize` just uses `pool.map` to execute a bunch of
statements in parallel. Using `functool`, I return a function that only needs
`sequence` as an input. It opens and closes a pool each time; certainly not
optimal but easy.

This method of parallelization seems prime for the scientific community. It's
short and sweet and doesn't require extensive modifications to the code. The
niche of the scientific community I'm part of often doesn't even use source
control, meaning that this method is *much* more attractive than the Java-like
methods in other packages.

We'll test a complicated and time-consuming function, a not-so-smart way to
test if a number is prime. We could use much smarter methods such as using
NumPy or even the  [Sieve of Eratosthenes][sieve], but let's pretend that this
is some much longer and more computation-intensive computation.


```python
def test_prime(n):
    prime = True
    for i in arange(2, n):
        if n/i % 1 == 0:
            prime = False
    return prime

for i in arange(N):
    serial[i] = test_prime(i)

test_prime.parallel = parallel_function(test_prime)
parallel_result = test_prime.parallel(arange(N))
```

Testing this parallelization out, we find that the results are *exactly* the
same, even with incredibly precise floats. This means that the *exact* same
computation is taking place, just on different cores.

Given the simplicity of including this parallelization, the most important
question to ask is about the speedup of this code. Like all complex subjects,
the answer is "it depends." It will primarily[^2] depend on the number of cores
your machine has. One core or worst case means that your parallelized code will
still run, just without the speed benefits.

On "basic" machines, such as this 4-core Macbook Air, I see parallelized results
that run about twice as fast. On an 8-core iMac, it's about 4 times as fast.
It seems like my operating system is only dedicating half the cores to this
process, but I don't want to dig into that magic.

Calling `test_primes.parallel` instead of `test_primes` gives us pretty large
speed gains for such a simple method. Even more convenient, editing the code to
do this was *easy.* Perhaps even better, it's easy to use threads instead of
processes. The `multiprocessing.dummy` module is an exact clone of
`multiprocessing` that uses threads instead of processes. Hence if you find
gains with threads (I didn't), use `from multiprocessing.dummy import Pool`.

If you're running code that takes a long time to run and can be run in
parallel, you probably should have access to a large supercomputing institute
like I should (but don't. Classic academia). Running code on machines [that
have 20 cores][20], we would expect to get results in 5% of the serial time.

[20]:https://www.msi.umn.edu/hpc

Too often, some promising example is shown that when applied in the real world
fails. To try and combat this, I decided to use a more complicated example,
calculating a [Mandelbrot set][mandel]. This can be natively parallelized using
NumPy, but I decided to simulate a more complex function. Once again, the
full code including serial and parallel declarations is 
[available on Github][source].

Calculating this Mandelbrot set relies on looping over a two-dimensional grid
(that is, without using NumPy). To parallelize this function, I essentially
only looped over one dimension while parallelizing the other dimension.

```python
def mandel_serial():
    m = zeros((N,N))
    i=-1;
    for x in linspace(-2, 1, num=N):
        i += 1
        j = -1
        for y in linspace(-2, 1, num=N):
            j += 1
            m[j,i] = mandel_pixel(x, y)
    return m # returns full mandelbrot set

def mandel_parallel(x):
    #m = zeros((N,N)) # reducing the dimension since called with `x`
    m = zeros(N); i=-1
    #for x in linspace(-2, 1, num=N): # called with `x`
    j = -1; i += 1
    for y in linspace(-2, 1, num=N):
        j += 1
        #m[j,i] = mandel_pixel(x, y)
        m[j] = mandel_pixel(x, y)

    return m # not the full mandelbrot set! only one row

mandel_p.parallel = parallel_attribute(mandel_p)
parallel = mandel_p.parallel(linspace(-2, 1, num=N))
parallel = parallel.T # dunno why; for parallel == serial
```

This edit is relatively simple. While I couldn't just have a drop in
replacement with `mandel.parallel`, some small edits to take out looping over
the `x` dimension made my function faster. Essentially, I brought the for-loop
over `x` outside the function. I see similar results with this code: about 2x
speedup on my 4-core and about a 4x speedup on the 8-core iMac.

At the end of the day, we can expect to easily parallelize our code providing
we use the right tools. This just involves making *small* edits for fairly
large speed gains (even on this machine!) and huge speed gains on
supercomputers.

If you want to see this in more detail, look [at the source][source] which is
well commented and works. In addition, I have written a [Binpress
tutorial][binpress] on how I discovered this function. To be complete, here are
the full results:

<!--[binpress]:http://www.binpress.com/XXXX-->

```
  Function      | Computer | Speedup | serial time (s) | parallel time (s)  
  --------------+----------+---------+-----------------+------------------- 
  Primes        | Air      | 2.63    | 2.16            | 0.82               
                | iMac     | 3.48    | 1.59            | 0.45               
  --------------+----------+---------+-----------------+------------------- 
  Mandlebrot    | Air      | 1.79    | 2.42            | 1.35               
                | iMac     | 3.53    | 2.51            | 0.71               
```

[^1]:The full source, including function declarations is [available on Github][source]

[^2]:If your input range is small like `range(1, 100)`, the overhead of creating the parallel function will wipe out any speed benefits. Luckily, your range is small enough this shouldn't matter.

[mandel]:https://en.wikipedia.org/wiki/Mandelbrot_set
[medium]:https://medium.com/building-things-on-the-internet/40e9b2b36148
[sieve]:https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
[ipy]:http://ipython.org/ipython-doc/dev/parallel/index.html
[parallel]:https://wiki.python.org/moin/ParallelProcessing
[multi]:https://docs.python.org/2/library/multiprocessing.html
[source]:https://github.com/scottsievert/scottsievert.github.io/blob/master/src/source/_posts/python-parallel/mandlebrot.py
[msi]:https://www.msi.umn.edu
[view]:http://ipython.org/ipython-doc/dev/parallel/parallel_multiengine.html#creating-a-directview-instance
[xkcd]:http://xkcd.com/927/

