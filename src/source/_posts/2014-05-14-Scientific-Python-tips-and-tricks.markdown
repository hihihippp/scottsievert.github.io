---
layout: post
title: "Scientific Python tips and tricks"
date: 2014-05-14 20:20:24 -0500
comments: true
categories: python
---

You want to pick up Python. But it's hard and confusing to pick up a whole new
framework. You want to try and switch, but it's too much effort and takes too
much time, so you stick with MATLAB. I essentially grew up on Python, meaning I
can guide you to some solid resources and hand over tips and tricks I've
learned.

<!--More-->

This guide aims to ease that process a bit by showing tips and tricks within
Python. This guide *is not* a full switch-to-Python guide. There are plenty of
resources for that, including [some wonderful SciPy lectures][scipy-lectures],
[detailed guides][scipy-lectures-http] to the same material, and 
[Python for MATLAB users][py-for-mat]. Those links are all useful, 
and **those links should be looked at.**

For an intro to Python, including types, the scope, functions and optional
keywords and syntax (string addition, etc), look at [the Python docs][python-docs].

But, that said, I'll share my most valuable tips and tricks I learned from
looking at the resources above. These do not serve as a complete replacement
those resources! I want to emphasize that.

### Installation
I recommend you install [Anaconda][anaconda]. Essentially, all this amounts to
is running `bash <downloaded file>`, but complete instructions can be found on
[Anaconda's website][install].

This would be easiest if you're familiar with the command line. The basics
involve using `cd` to navigate directories, `bash <command>` to run files and 
`man <command>` to find help, but more of the basics can be found
[with this tutorial][bash-basics].

### Interpreters
The land of Python has many interpreters, aligning with the [Unix philosophy][unix].
But at first, it can seem confusing: you're presented with the default python
shell, [bpython][bpy], IPython's shell, [notebook][notebook] and [QtConsole][qt].

I most recommend IPython; they seem to be more connected with scientific
computing. But which one of IPython's shells should you use? They all have
their pros and cons, but the QtConsole wins for plain interpreters.
[Spyder][spyder] is an alternative (and IDE, meaning I haven't used it much)
out there that tries to present a MATLAB-like GUI. I do know 
[it's possible to have IPython's QtConsole in Spyder][spyder-qt].

*EDIT: Apparently IPython's QtConsole is included by default now.*

##### QtConsole
This is what I most highly recommend. It allows you to see plots inline. Let me
repeat that: *you can plot inline*. To see what I mean, here's an example:

{% img right http://ipython.org/ipython-doc/stable/_images/qtconsole.png 350 %}

I've only found one area where it's lacking. The issue is so small, I won't
mention it.

##### Notebook
Great for *sharing* results. Provides an interface friendly to reading code,
$\LaTeX$, markdown and images side-by-side. However, it's not so great to
develop code in.

#### IPython magic
Normally in Python, you have to run `attach(filename)` to run an object. If you
use IPython, you have access to `%run`. I've found it most useful for
inspecting global variables after the script has run. IPython even has other
useful tools including `%debug` (debug *after* error occured acting like it
*just* occured),
`!<shell-command>` and `function?`/`function??` for help on a function. The
[docs on magics are handy][magic].

#### My personal setup 
I typically have MacVim and IPython's QtConsole (using 
[a special applescript][applescript] 
to open; saves opening up iTerm.app) visible and open
with an external monitor to look at documentation. A typical script look like

```python
from __future__ import division
from pylab import *

N = 1024
x = linspace(-1, 1, num=N) # make vector from -1 to 1 with N components
y = linspace(-1, 1, num=N)
x, y = meshgrid(x, y)
z = x**2 + pow(y, 2) # ** and pow(y, 2) are equivalent

figure()
imshow(z, interpolation='nearest') # interpolation for no fuzziness
colorbar()
savefig('z.png', dpi=300)
show()
```

I can then run this script in IPython's QtConsole with `%run script.py` (using
a handy [Keyboard Maestro][keyboard-maestro] shortcut to switch windows and
enter %run) and then can query the program, meaning I can type `z` in the
QtConsole and see what `z` is or even `plot(z[0,:])`. This is a simple script,
but this functionality is priceless in larger and more complicated scripts.

### pylab
[Pylab's][pylab] goal is to bring a MATLAB-like interface to Python. They
largely succeed. With pylab, Python can *almost* serve as a drop-in replacement
for MATLAB. You call `x = ones(N)` in MATLAB; you can do the same with pylab.

One area where it isn't a drop-in replacement is with division. In Python 2,
`1/2 == 0` through integer division and in MATLAB (and the way it should be),
`1/2 == 0.5`. In Python, if `int/int-->int` is wanted, you can use `1//2`
instead.

To present a nearly drop-in MATLAB interface, use the following code

```python
from __future__ import division
from pylab import *
```

This `from pylab import *` is frowned upon. The [Zen of Python][zen] says

> Namespaces are a honking great idea -- let's use more of those!

meaning that `from package import *` shouldn't be used *with any package.* It's
best to use `import pylab as p` but that's kinda annoying and gets messy in
long lines with lots of function calls.  I use `from pylab import *`; I'm
guesing you'll do the same.  If I'm wondering if a function exists, I try
calling it and see what happens; oftentimes, I'm surprised.

### Parallelism
Parallelism is a big deal to the scientific community: the code we have takes
hours to run and we want to speed it up. Since for-loops can be sped up a ton
by parallelism if each iteration is independent, there are plenty of
parallelization tools out there to parallelize code, including 
[IPython's paralleziation toolbox][ipy-parallel].

But, this is still slightly confusing and seems like a pain to execute. I
recently stumbled across on 
[a method to parallelize a function in one line][parallel-oneline]. Basically,
all you do is the following:


```python
# serial
x = []
for i in arange(10):
    x += [function()]

# parallel
from multiprocessing import Pool
x = pool.map(function, arange(10)) # normally `for i in arange(10): function()`
pool.close()
pool.join()
```

[The link above][parallel-oneline] goes into more detail; I'll omit most of it.
IPython's parallelization toolkit [also includes a `map()` interface.][map]

*UPDATE:* see [my blog post on how to parallelize easily](http://scottsievert.github.io/blog/2014/07/30/simple-python-parallelism/)

### SymPy (+LaTeX printing!)
[SymPy][sympy] serves as a replacement for Mathematica (or at least it's a
close race). With SymPy, you have access to symbolic variables and can perform
almost any function on them: differentiation, integration, etc. They support
matrices of these symbolic variables and functions on them; it seems like a
complete library.

Perhaps most attractive, [you can even pretty print LaTeX or ASCII][pprint].

{% img left http://docs.sympy.org/latest/_images/ipythonqtconsole.png 400 %}

I haven't used this library much, but I'm sure there are good tutorials out
there.

### Indexing
When indexing a two-dimensional numpy array, you often use something like
`array[y, x]` (reversed for good reason!). The first index `y` selects the
*row* while the second selects the *column.*

For example,

```python
x = arange(4*4).reshape(4,4) # make 4x4 matrix
print x
 #  [[ 0  1  2  3]
 #   [ 4  5  6  7]
 #   [ 8  9 10 11]
 #   [12 13 14 15]]

print x[1,:] # selects 2nd row (0-based indexing) and every column
 # [4, 5, 6, 7]

print x[:,2] # selects 3rd column and every row
 # [2, 6, 10, 14]

print x.T.flat[0, 1, 2, 3]
 # [0, 4, 8, 12]

print x.flat[0, 1, 2, 3]
 # [0, 1, 2, 3]
```

This makes sense because you'd normally use `x[0][1]` to select the element in
the 1st row and 2nd column. `x[0,1]` does the same thing but drops the
unnecessary brackets. This is because Python selects the first object with the
first index. Looking at our array, the first object is another array and the
first row.

In MATLAB, indexing is 1-based but perhaps most confusingly `array(x,y)` is
`array[y,x]` in Python. MATLAB also has a feature that allows you to select an
element based on the total number of element in an array. This is useful for
the [Kroeneker product][kron]. MATLAB stacks the columns when doing this, which
is exactly the method `kron` relies on. To use Kroeneker indexing in Python, I
use `x.T.flat[i]`.

### `@`: Dot product operator
In any Python version <= 3.4, there's no dot
product operator unlike MATLAB's `*`. It's possible to multiply an array
element-wise easily through `*` in Python (and `.*` in MATLAB). But coming in
Python 3.5 is a new dot product operator! The choices behind `@` and the
rational are [detailed in this PEP][@].

Until the scientific community slowly progresses towards Python 3.5, we'll be
stuck on lowly Python 2.7. Instinct would tell you to call `dot(dot(x,y), z)`
to perform the dot product of $X \cdot Y \cdot Z$. But instead, you can use
`x.dot(y).dot(z)`. Much easier and much cleaner.

### Version Control
This is not really related to the scientific programming process; it applies to
any file, whether it be in a programming language or not (a good example: 
LaTeX files).

Stealing from [this list][version-control], if you've ever

* made a change to code, realised it was a mistake and wanted to revert back?
* lost code or had a backup that was too old?
* had to maintain multiple versions of a product?
* wanted to see the difference between two (or more) versions of your code?
* wanted to prove that a particular change broke or fixed a piece of code?
* wanted to review the history of some code?
* wanted to submit a change to someone else's code?
* wanted to share your code, or let other people work on your code?
* wanted to see how much work is being done, and where, when and by whom?
* wanted to experiment with a new feature without interfering with working code?

then you need version control. Personally, I can't imagine doing anything
significant without source control. Whenever I'm writing a paper and working on
almost any programming project, I use `git commit -am "description"` all the
time. Source control is perhaps my biggest piece of advice.

Version control is normally a bit of a pain: you normally have be familiar with the
command line and (with CVS/etc) it can be an even bigger pain. Git (and it's
brother Github) are considered the easiest to use versioning tool.

They have a GUI to make version control *simple*. It's simple to commit changes
and roll back to changes and even branch to work on different features. It's
available for [Mac][git-mac], [Windows][git-win] and [many more GUIs][git-guis]
are available.

They even offer [private licenses for users in academia][gh-academia]. This
allows you to have up to five free *private* code repositories online. This
allows for easy collaboration and sharing (another plus: access to 
[Github Pages][gh-pages]). There's [a list of useful guides][gh-tutorial] to
getting started with Git/Github.

### drawnow
(shameless plug) MATLAB has a great feature that allows you to call `drawnow`
to have a figure update (after calling a series of plot commands). I searched
high and low for a similar syntax in Python. I couldn't find anything but
matplotlib's animation frameworks which didn't jive with the global scope ease
I wanted to use. After a long and arduous search, I did find `clf()` and
`draw()`. This is simple once you know about it, but it's a pain to find it.

So, I created [python-drawnow][drawnow] to make this functionality *easily*
accessible. It easily allows you to view the results of an iterative (aka
for-loop) process.

### Conclusion
As I stressed in the introduction, this guide is not meant to be a full
introduction to Python; there are plenty of other tools to do that.
[There][scipy-lectures] [are][scipy-lectures-http] [many][py-for-mat]
[other][tutorials] [tutorials][python-docs] on learning Python. These all cover
the basics: syntax, scope, functions definitions, etc. And of course, the
documentation is also a great place to look ([NumPy][numpy-doc],
[SciPy][scipy-doc], [matplotlib][mpl-doc]). Failing that, a
Google/stackoverflow search will likely solve your problem. Perhaps the best
part: if you find a problem in a package and fix it, you can commit your
changes and make it accessible globally!

[magic]:http://ipython.org/ipython-doc/dev/interactive/tutorial.html
[mat-py-hack]:http://stackoverflow.com/questions/17445995/how-to-call-multiple-functions-from-a-single-m-matlab-file
[full-ide]:https://wiki.python.org/moin/IntegratedDevelopmentEnvironments
[sci-ide]:http://xcorr.net/2013/04/17/evaluating-ides-for-scientific-python/
[code-speed]:https://github.com/scottsievert/side-projects/tree/master/matlab_v_python_v2
[speed]:https://modelingguru.nasa.gov/docs/DOC-1762
[perf-py]:http://wiki.scipy.org/PerformancePython
[julia]:http://julialang.org
[numba]:http://numba.pydata.org
[numpy-gh]:https://github.com/numpy/numpy
[bash-basics]:http://mac.appstorm.net/how-to/utilities-how-to/how-to-use-terminal-the-basics/
[gh-tutorial]:https://help.github.com/articles/what-are-other-good-resources-for-learning-git-and-github
[gh-pages]:https://pages.github.com/
[gh-academia]:https://education.github.com/
[keyboard-maestro]:http://www.keyboardmaestro.com/main/
[python-docs]:https://docs.python.org/2/tutorial/introduction.html
[applescript]:http://apple.stackexchange.com/questions/84348/how-can-i-create-a-stand-alone-app-to-run-a-terminal-command
[zen]:http://legacy.python.org/dev/peps/pep-0020/
[git-guis]:http://askubuntu.com/a/227566
[git-win]:https://windows.github.com/
[git-mac]:https://mac.github.com/
[version-control]:http://stackoverflow.com/a/1408464
[mpl-doc]:http://matplotlib.org/contents.html
[scipy-doc]:http://docs.scipy.org/doc/
[numpy-doc]:http://docs.scipy.org/doc/
[anaconda]:http://docs.continuum.io/anaconda/
[drawnow]:https://github.com/scottsievert/python-drawnow
[@]:http://legacy.python.org/dev/peps/pep-0465/#implementation-details
[kron]:https://en.wikipedia.org/wiki/Kronecker_product
[pprint]:http://docs.sympy.org/latest/tutorial/printing.html
[sympy]:http://sympy.org/en/index.html
[map]:http://ipython.org/ipython-doc/dev/parallel/asyncresult.html#map-results-are-iterable
[parallel-oneline]:https://medium.com/building-things-on-the-internet/40e9b2b36148
[ipy-parallel]:http://ipython.org/ipython-doc/dev/parallel/index.html
[spyder-qt]:http://pythonhosted.org/spyder/ipythonconsole.html
[spyder]:https://code.google.com/p/spyderlib/
[bpy]:http://bpython-interpreter.org/
[notebook]:http://ipython.org/notebook.html
[qt]:http://ipython.org/ipython-doc/stable/interactive/qtconsole.html
[install]:https://store.continuum.io/cshop/anaconda/
[unix]:https://en.wikipedia.org/wiki/Unix_philosophy
[pylab]:http://wiki.scipy.org/PyLab
[scipy-lectures-http]:http://scipy-lectures.github.io
[scipy-lectures]:https://github.com/jrjohansson/scientific-python-lectures
[py-for-mat]:http://wiki.scipy.org/NumPy_for_Matlab_Users
[tutorials]:http://www.scientificpython.net/
