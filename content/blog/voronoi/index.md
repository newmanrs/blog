+++
title = "Blog now with better plot support"
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

Working on getting plotly.js charts into the blog.

<!--more-->

### Plots

Guess since I'm implementing charts here, I'll just make a few applied math classics.

### Lotka-Volterra ODE system

The [Lotka-Volterra model](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations) is one of the simplest predator-prey dynamics models that has a stable limit cycle, meaning that the system enters a permanent oscillatory pattern.  It consists of a population of prey $x(t)$ that grows exponentially with growth rate $\alpha$, a predator $y(t)$ that starves exponentially with death rate $\gamma$, and interaction terms of predation proportional to the population of both.

$ \frac{dx}{dt} = \alpha x - \beta xy $,

$ \frac{dy}{dt} = \delta xy - \gamma y $

where $\alpha$, $\beta$, $\delta$, $\gamma$ are positive constants.  This coupled system of equations has a stable limit cycle that includes the initial population.  The chart that follows is of the Lotka-Volterra system with $\alpha = 2/3$, $\beta=4/3$, $\gamma=1$, $\beta=1$, and integrated numerically from $t=0$ to $t=20$ with step size $\Delta t=0.05$.


{{< include-html "lotkavolterra.html" >}}
