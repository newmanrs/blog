+++
title = "Blog now featuring interactive plots"
date = 2021-12-06
draft = false
categories = ["plotly", "ode"]
removeBlur = false
plotly = true

#[[images]]
# src = "/blog/voronoi-image-compression/featured.png"
# alt = "Cloudburst beers containing Azacca"
# stretch = true
+++

Testing out some plotly.js charts into the blog by going straight for animations of systems of differential equations.

<!--more-->

### Plots

Suppose now that I've edited this site to support [plotly](https://plotly.com/javascript/), I should produce some content with them.  Time plot and animate some applied math classics.

### Lotka-Volterra ODE system

The [Lotka-Volterra model](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) is one of the simplest predator-prey dynamics models demonstrating stable limit cycle, meaning that the system enters a fixed oscillatory pattern. 
It consists of a population of prey $x(t)$ that grows exponentially with growth rate $\alpha$, a predator population $y(t)$ that starves exponentially with death rate $\gamma$, and interaction terms of predation causing the growth of the predators and deaths of the prey proportional to the product of their populations (more hungry predators eat more available prey).  This system is defined as:

$$ \frac{dx}{dt} = \alpha x - \beta xy ,$$
$$ \frac{dy}{dt} = \delta xy - \gamma y ,$$

and where $\alpha$, $\beta$, $\delta$, $\gamma$ are positive constants.
The chart that follows is of the Lotka-Volterra system with $\alpha = 2/3$, $\beta=4/3$, $\gamma=1$, $\beta=1$, and integrated numerically from $t=0$ to $t=20$ with step size $\Delta t=0.05$.

{{< include-html "lotkavolterra.html" >}}

Different initial conditions to this particular system of ODEs give rise to a family of limit cycles that return to pass through the initial point.  The math or wikipedia inclined can eliminate t from the equations, separate and integrate to realize $f(x,y)$ for some constant $V$ and function $f$.
So onwards to a more complex example.

<!--

Iframe embedding, with plotly exporting its own cdn hits allows for mathjax to work with both the plot and mathjax in the post, but that seems excessively heavy/janky.  Just live without mathjax in the images for now.  Even if I get it to work it'll break in the future.

<iframe width="100%", height=500 name="iframe" frameborder=0 src="lotkavolterra.html"></iframe>

-->


## Van der Pol Oscillator

A common oscillator studied by applied mathematicians is that of Balthasar van der Pol, describing an electrical circuit discussed in his paper ["Frequency Demultiplication (1927)"](https://www.nature.com/articles/120363a0).  He found an oscillatory circuit that could reduce the frequency of inputs $\omega$ by integers, that is $\frac{\omega}{2}, \frac{\omega}{3} \frac{\omega}{4} ...$.  Van der Pol notes that tuning a capacity to switch these frequencies allows his circuit to play music minor scales, with the caveat that "strongly reminds one of the tunes of a bagpipe".

TODO CIRCUIT DIAGRAM


{{< include-html "vanderpol.html" >}}






## Plotly rambling review / rant

Honestly it's better than the initial look at the documentation would suggest.  The python package was clearly originally a thin port of the javascript API, so many of the examples are just python scripts builting deep nested dictionaries hundreds of lines long and pushing it to a make figure object.  It makes it pretty hard to rationalize what is going on or debug and edit.

For those of you who want to use it in static webpages like I am be wary that the use of Mathjacs in the page and the figures is problematic.  It works if you separate the plots into individual iFrames, but for my uses I think it wasn't worth it to have marginally better figure labels.





