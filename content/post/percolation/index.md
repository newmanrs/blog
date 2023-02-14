+++
title = "Percolation"
date = 2021-01-01
draft = false
categories = ["percolation", "plotly", "phase transition", "statistical physics"]
removeBlur = false
plotly = true

[[images]]
 src = "/blog/percolation/featured.jpg"
 alt = "My 1991 Merlin alongside a building facade featuring a random waterjet cut motif"
 stretch = true
+++

Bicycle ride inspired blog post.  Not often do I see statistical physics waterjet cut into building facades.

<!--more-->

### Percolation

Article is just a stub for now to test/share the plot below, and verify that it works when pushed live to the website (as well as test its performance.  This text is also an attempt to stall the few testers to not noticing that the play button doesn't work until the few megabytes of data composing the animation load.  And if you're curious, the 2500 mouseover labels is probably most of the figure.

{{< include-html "animate_2500.html" >}}

### Todo - fix bugs:

Figure out if I can get the blog reading timer feature to resolve based on the length of these markdown posts before HTML/Javascript gets embedded inside of them.  Suppose some dedicated reader could in theory read each pixel mouseover of each frame of the plot... seems unlikely.

### Plot Code

Code for the plot is on my [Github](https://github.com/newmanrs/blog/blob/main/content/blog/percolation/percolation.py).
