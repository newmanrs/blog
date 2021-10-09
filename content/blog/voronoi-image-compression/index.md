+++
title = "Voronoi Image Compression"
date = 2021-09-27
draft = true
categories = ["pagebundle"]
removeBlur = false

[[images]]
 src = "/blog/voronoi-image-compression/featured.png"
 alt = "Cloudburst beers containing Azacca"
 stretch = true
+++

Goofing around with voronoi tesselations of images inspired by this [code golf question](https://codegolf.stackexchange.com/questions/50299/draw-an-image-as-a-voronoi-map) I bookmarked years ago.

<!--more-->

# Introduction to Voronoi diagrams

Voronoi cells are the region of space closest to a given point in a set of points.


Mathematically, a voronoi cell $C_i$ around a point $p_i with distance function $d$ is defined as

$$ C_i = { x \in R^2 | d(x,p_i) < d(x,p_k) \forall i \neq j} $$


# Hello

Hello

![Stuff](azacca.png "Stuff")



[Hello](https://linktosomewhere)

# Test image galleries

Gallery!

default pix height
{{< foldergallery folder="imgs">}}

100px height
{{< foldergallery folder="imgs" height="100px" >}}

50px
{{< foldergallery folder="imgs" height="50px" >}}



{{< foldergallery folder="gallery2" height="250px">}}
