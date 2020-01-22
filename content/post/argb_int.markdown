---
title: "Converting argb to int"
date: 2020-01-07T16:39:32-08:00
draft: False
---

Apparently a lot of my old computer simulations inconsistently store RGB color either as separate values or as a single integer.  I figure I might as well write a post so I don't continue to forget how to do the conversions.

<!--more-->

The main gist is that to save a trivial amount of space in file formats our old simulation engine would pack four 8-bit integers into a 32 bit integer before writing it out as plaintext.  Perhaps it would have been wiser to write out in standard hexadecimal, but scientific software is oft in need of a refactor.  I suppose the problem often lies in the fact that scientists and grad-students are paid to produce research and not to craft great software.  In fact, some of my former labmates have [wrote a paper discussing this](https://doi.org/10.1109/MCSE.2018.2882355).  But I digress...










```python


```python


```
