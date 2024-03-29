---
title: "Revisiting the fibonacci sequence"
date: 2018-03-23T12:13:50-07:00
draft: true
---

While cleaning out my desk I found some notes on the Fibonacci sequence which I figured I might want to keep, and/or some other people might find interesting.  These were initially due to examining a particularly poor algorithmic implementation, which will be discussed later.

Informally, the Fibonacci sequence is defined as the sum of the two preceding numbers, starting from 1 and 1.  That is, 1, 1, 3, 5, 8, 13, 21 and so forth.  Formally, this sequence is described by the difference equation:

\\[ F(n+1) = F(n) + F(n-1), \\]

where we have initial conditions $$F(0)=0,F(1)=1$$, and this relation can be applied iteratively to generate the sequence.

<!--more-->

## Notation

To prevent clutter when writing out analysis, I will be using the shorthand $$F_n = F(n)$$, and for the most part assume $$n$$ to be a positive integer. So to restate in this notation (and shifting the indices):

$$F_n = F_{n-1} + F_{n-2}$$

where we have initial conditions $$F_0=0,F_1=1$$.

For those who are new to this notation this works out as

$$ F_2 = F_1 + F_0 = 1 + 1 = 2 $$

$$ F_3 = F_2 + F_1 = 2 + 1 = 3$$

and so forth.

# Rate of growth of the sequence

I suppose first let's just tackle this with some old fashioned math.  A retrospectively great initial question is to ask how fast does this sequence numbers of grow. That is, how does the ratio of successive terms $$\frac{F_{n}}{F_{n-1}}$$ behave?

We need a point of attack, so lets consider dividing through our difference equation by $$F_{n-1}$$, to get some of these ratios of terms to appear and take the limit as n grows large.

$$ \lim_{n\to\infty} \frac{F_{n}}{F_{n-1}} = \lim_{n\to\infty}1 +\frac{F_{n-2}}{F_{n-1}}$$

Lets just boldy proceed assuming that the limit of $$\frac{F_n}{F_{n-1}}$$ exists and denote it $$l$$.  Then we have:

$$ l = 1 + \frac{1}{l}$$

$$ l^2 -l -1 = 0 $$

Note that the assumption of the limit of successive terms existing implies $$\frac{F_n}{F_{n-1}} = \frac{F_{n-1}}{F_{n-2}}$$.  Solving the quadratic gives two roots:

$$ l_1 = \tfrac{1 +\sqrt{5}}{2} = 1.618...$$

$$ l_2 = \tfrac{1 -\sqrt{5}}{2} = -0.618...$$

The positive root of this is $$ l_1 $$ is the golden ratio usually denoted $$\phi$$.
Since we know that the $$F_n$$ is an increasing it follows that that $$l_1$$ is the relevant bounds on the growth rate.

$$ \lim_{n\to\infty} \frac{F_{n}}{F_{n-1}} = \frac{1 + \sqrt{5}}{2} $$

So if the limit exists, then this function grows exponentially.
Pedants will note that since this function is discrete, its more fair to say it grows geometrically as it grows by a constant ratio.
They are probably correct, but the terminology seems less often used.  Many more people may find it strange that an integer-valued sequence can grow by a constant ratio that is an also an irrational number, which I suppose is good justification for scribbling out math now and then!

## Numerical Checkpoint

When you can check numerically... check numerically.




# Derivation of analytic solution

With candidates for geometric roots, lets see if we can derive a formula for directly calculating the $n$-th Fibonacci number, and call this function $$\mathcal{F}(n)$$.  This notation is to distinguish it from the difference equation above (which must be applied iteratively), although $$\mathcal{F}(n) = F_n$$.

An entirely reasonable guess for the functional form for $$\mathcal{F}(n)$$ is to use the two roots found above:

$$\mathcal{F}_n = A l_1^n + B l_2^n $$

or

$$ \mathcal{F}_n = \frac{A (1+\sqrt{5})^n + B (1-\sqrt{5})^n}{2^n} $$

Then we attempt to match the initial conditions. Inserting $$F_0 = 1 $$ gives

$$ A + B = 1 \implies B = A-1 $$

and 

$$ F_1 = 1 \implies \frac{A (1+\sqrt{5}) + B (1-\sqrt{5})}{2} = 1$$

Substituting, etc. and solving for A, B is straightforward but too tedious to typeset fully gives:

$$ A = \frac{1+\sqrt{5}}{ 2\sqrt{5}} $$

$$ B = 1 - A \implies B = 1 - \frac{1+\sqrt{5}}{ 2\sqrt{5}}$$

Rearranging,

$$ B = -\frac{1-\sqrt{5}}{2\sqrt{5}} $$

And now we have an analytical formula for n-th Fibonacci number, namely:

$$ \mathcal{F}(n) = \frac{(1+\sqrt{5})^{n+1} - (1-\sqrt{5})^{n+1}}{2^{n+1}\sqrt{5}} $$

At first glance I would say this fails a sanity check since it seems highly unlikely that for a given value of $$n$$ that this would yield an integer.  However, it turns out upon expansion the symmetry of the numerator eliminates all even powers of $$\sqrt{5}$$, and all remaining coefficients are divisible by $$2^{n+1}$$.

TO SELF:  Is that obvious? I don't remember this expansion, and if so, it was confiscated and discarded by Ada Mohedano after I left the SCCA.  To future self: Do not leave notes on desk when resigning positions.

## Mildy interesting aside

One might ask what values of $$a$$ in the related, but more generic function,

$$ G(n) = \frac{(1+a)^{n} - (1-a)^{n}}{a 2^{n}} $$

yield integer values for all values of $$G(n)$$.

This appears to hold when $$a$$ is odd or $$a=\sqrt{4m+1}$$ where $$m$$ is a nonnegative integer.

I may revisit this in a future post if I end up reinstalling a computer algebra system.

# So why were these notes on my desk?

For those curious, the actual reason these notes on the Fibonacci sequence were on my desk in the first place is I was analyzing the runtime of the awful implementation of the fibonacci sequence that calls itself recursively.

Computer scientists will tell you the runtime is obviously exponential, and decline to give the exact bounds since they remember it as fact, and generally only with finding upper bounds of performance (see big O notation and analysis TODO: PROVIDE LINK).

Haskell:
```haskell
fib 0 = 1
fib 1 = 1
fib n = fib (n-1) + fib (n-2)
```

Python:
```python
def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1)+fib(n-2)
```

This is a terrible implementation, since to call `fib(10)` we invoke calls to `fib(9)` and `fib(8)`, each of which branch further.  In a short pencil exercise of drawing the tree the number of function calls to `fib(n)` in these implementations is $$2\mathcal{F}(n)-1 $$.

The difference equation that generates the counts of the functional calls to `fib(n)` turns out to be an inhomogeneous variant of the Fibonacci sequence (jargon for adds a constant to the equation):

$$ g_n = g_{n-1}+g_{n-2} + 1 $$

A similar argument to the growth rate discussed above shows that this is also has growth bounded by the golden ratio (although this must be true, if the solution to this $$ g(n) = 2 \mathcal{F}(n)-1$$.  While one of the least efficient ways to compute $$\mathcal{F}(n)$$, it is quite elegant in that its performance bounds its value.

Considering an arbitrary constant $$c$$ in the difference equation

$$ h_n = h_{n-1}+h_{n-2} + c $$

with $$h_0 = h_1 = 1$$ has solution

$$ h(n) = (c+1)\mathcal{F}_n-c $$

This curiously appears to hold for both positive and negative real numbers $$c$$.

 This might be the only novel part of the post, although I'm sure some mathematicians have previously solved for this more rigorously since it's the simplest possible inhomogeneous linear difference equation.  Although at this point, I don't know that many people who actually would solve such a thing rigorously.

## Other ways to compute the sequence 

### Another terrible way

Paul Hankin discusses an interesting (but thoroughly impractical) method using bitwise operators and provides the implementation reprinted here:  

```python
def fib(n):
    return (4 << n*(3+n)) // ((4 << 2*n) - (2 << n) - 1) & ((2 << n) - 1)
```

Unlike the common analytical form derived above, at least this is plausibly integer valued.
http://paulhankin.github.io/Fibonacci/

### A useful way

Discuss or show the matrix exponentiation way.  It's sweetly O(log(n)) instead of linear so it's better than the naive solution. 


### Benchmarks?

Compute some benchmarks?  Maybe not worth writing good implementations
