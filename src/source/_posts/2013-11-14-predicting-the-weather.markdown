---
layout: post
title: "Predicting the weather"
date: 2013-11-14 10:44:33 -0500
comments: true
categories: 
---


Let's say that we're accurately measuring the temperature in both Madison and Minneapolis, but then our temperature sensor in Minneapolis breaks. We could easily install a new sensor, but we would prefer to estimate the temperature in Minneapolis based on the temperature in Madison. 

First, let's see the temperature difference between the two cities:

$
\newcommand{\ex}[1]{\mathbb{E}\left[ #1 \right]}
$

<!--![Temperature difference](https://raw.githubusercontent.com/scottsievert/side-projects/master/predicting_weather/temp_diff.png)-->

{% img center https://raw.githubusercontent.com/scottsievert/side-projects/master/predicting_weather/temp_diff.png 500 %}

Let's say we're collecting the data accurately and are free from the effects of noise. So, let's gather the data. In this, we're estimating $X$ from $Y$. The mean temperature difference, or in math terms, $\ex{\left\|X-Y\right\|} = 4.26^\circ$ ($\ex{\cdot}$ is an operator that finds the mean).

We're going to a linear estimation process. This process only takes in
information data about the current data and nothing about the general trend of
the seasons. This process just says that the temperature in Minneapolis is 80%
of the temp in Madison plus some constant; fairly simple. Regardless, it's still
pretty good as Madison and Minneapolis are fairly similar for temperature. The
only thing this estimation requires is some past weather data in Minneapolis to
predict the mean $\ex{X}$ and variance $\propto \ex{X^2}$ nothing more.

We want to minimize the *energy* of the error, using the $l\_2$ norm. This
choice may seem arbitrary, and it kind of is. If this data were sparse (aka
lots of zeros), we might want to use the $l\_1$ or $l\_0$ norms. But if we're
trying to minimize cost spent, the $l\_0$ or $l\_1$ norms don't do as good of a
job minimizing the amount of dollars spent.

But doing the math,

$$ \min \ex{\left(X-(\alpha Y+\beta)\right)^2} = \\\\\min \ex{X^2} +
\alpha^2\ex{X^2} + \beta^2 + 2\alpha\beta\ex{X} - 2\alpha\ex{XY} - 2\beta\ex{X}  $$

Since this function is concave (or U-shaped) and $\ex{\cdot}$ a linear function, we can minimize it using derivates on each term.

$$\frac{d}{d\alpha} = 0 = -2 \ex{XY} + 2 \alpha\ex{Y^2} + 2\beta \ex{y}$$

$$\frac{d}{d\beta} = 0 = -2 \ex{X} + 2\beta + 2\alpha\ex{X}$$

This linear system of equations is described by $Ax = b$ or 

$$
\begin{bmatrix} \ex{Y^2} & \ex{Y} \\\\ \ex{X} & 1 \end{bmatrix}
\cdot
\begin{bmatrix} \alpha~/~2 \\\\ \beta~/~2  \end{bmatrix}
=
\begin{bmatrix} \ex{XY}\\\\ \ex{X}\end{bmatrix}
$$

Solving this linear system of equations by multiplying $A^{-1}$ gives us

$$\alpha = 0.929\\\\\beta = 3.14 $$

On average, the temperature in Minneapolis 92.9% of Madison's, plus 3 degrees.
Let's see how good our results are using this $\alpha$ and $\beta$. The
temperature difference between the two cities, but predicting one off the other
is shown below:

<!--![After prediction](https://raw.githubusercontent.com/scottsievert/side-projects/master/predicting_weather/pred_diff.png)-->
{% img center https://raw.githubusercontent.com/scottsievert/side-projects/master/predicting_weather/pred_diff.png 500 %}

That's *exactly* what we want! It's fairly close to the first graph. While
there are areas it's off, it's pretty dang close. In fact, on average it's
within $4.36^\circ$ -- fairly close to the original on average temperature
difference of $4.26^\circ$!

