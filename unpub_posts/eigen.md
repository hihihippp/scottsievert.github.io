* XKCD
* fixed point iteration
* digitalization
* fibonacci
* stability
* nonlinear

The mathematics of [XKCD #688] are interesting. I have implemented it but I did not fully understand the mathematics behind it and have since learned more of the mathematics that apply.

<!--images-->

This is an iterative process. Running the code

```
x = get_base_image()
while True:
    x = process_image(x)
```

will give us our image. In [my implementation] below, we can see that this works.

<!--image-->

How do we describe this mathematically? We know that it's just a linear function, so we can just do $x_1 = A x_0$ where $x_0$ is the original image without all the bars/charts/etc. But then $x_2 = A x_1 = A \cdot A \cdot x_0 = A^2 x_0$. Generally, we can say that $x_k = A^k x_0$. This is [fixed point iteration], but you don't need to know that in detail.

Let's take a simpler example of computing the Fibonacci numbers. As you may not, $x_k = x_{k-1} + x_{k-2}$ with $x_0 = 0$ and $x_1 = 1$. A typical implementation would look something like

```
x_k_2 = 0 # x of k minus 2
x_k_1 = 1 # x of k minus 1

# calulate the 100th fibonacci number
for i in arange(100):
    x_k = x_k_1 + x_k_2
    (x_k_1, x_k_2) = (x_k, x_k_1)
```

Expressing this in mathematical terms, we could just do $ x_k = x_{k-1} + x_{k-2} $ or applying it in matrix form so this cool theory applies,

$$
\begin{bmatrix}
x_k \\
x_{k-1} \\
\end{bmatrix}
=
A \cdot x
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

This is expensive time-wise for something so small. For this Fibonacci sequence generator, this would require $O(k)$ operations. This $O(k)$ is almost as bad as much more powerful functions such as the FFT which requires $O(n\log n)$ operations for an $n$ dimensional signal. For fixed point iteration with matrices (e.g., XKCD image) this would require $O(kn^3)$ operations for in $n\cross n$ matrix -- matrix multiplication is expensive.

We want to reduce the time of this fixed point iteration. One convenient way is to diagonalize the matrix. Why? Because this would just square the entries $k$ times. That is,

$$
\Lambda \cdot \Lambda \cdot \ldots \cdot \Lambda = \Lambda^k = 
 \begin{bmatrix}
   \lambda_{_1}^k                                      \\
    & \lambda_{_2}^k   &  &   \text{\huge0}             \\
    &                  & \ddots        &                 \\
    &                 &             & \ddots \\
    & \text{\huge0}    &               &  & \lambda_{_n}^k & \\
 \end{bmatrix}
$$

But how do we choose $Q$ and $\Lambda$? It turns out these are chosen by the eigenvectors and eigenvalues respectively, but do not be scared by those words. This blog post is not about *how* eigen works but the effects of it working. If you want to learn more, [there] [are] [many] [tutorial] available.






