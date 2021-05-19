---
title: "Graph data and graph databases"
date: 2018-06-19T13:28:54-07:00
draft: true
---

Waxing on some data modeling philosophy on graph databases

<!--more-->

# Introduction

Graph databases appear to be an increasingly trendy way to store data for different projects, and I'm relieved that the state of the database field to have any contenders to the behemoth of traditional SQL.  


At the risk of committing blasphemy across corporate America I will say that this is not often the best solution for storing business data:  it is merely the only used solution with historical origins in the early 1970s.  

<!--more-->

Before we talk about the details of relational and graph databases, I suppose we should keep in mind why we even use databases at all.  The obvious business use case:  We need to store data reliably, somewhere.  This has many candidate solutions, so we may want to understand what 'reliably' means.  I would take this to mean that we would want to be update the data in a fault-tolerant manner, preferably (but not necessarily) scalable to large systems, and also allow for reliable snapshotting (saving and loading to disk).  The chief reason to store data in most traditional databases is they implement fault tolerant data modification and storage.  In the modern era these are frequently referred to as the ACID properties (Atomicity, Consistency, Isolation, Durability).  These are pretty ancient ideas, for example see [Haerder and Reuter 1983](https://dl.acm.org/citation.cfm?doid=289.291) for a discussion of databases possessing these kinds of properties.

Briefly, atomicity means a set of operations can be performed on the database that either succeeds fully, or fails fully (returning the data to the prior state).  Isolation means several of these atomic operations can occur at once.  Consistency means the state of the database is known not to be corrupt and obeys whatever rules the database system has put forth to constrain the data format, and durability is given by a fault-tolerant log that means data integrity can survive hardware or power failures.

This is pretty far away from the design philosophy of high performance computing that I did during graduate school.  There the ACID properties on manipulating data would be considered computationally burdensome, although as parallel simulations scale out across larger and larger clusters I expect fault tolerance will eventually become a concern.  I.e. if the failure of a given node (computer) during the simulation runtime is $$ P(\text{failure}) $$, then the odds of a successful simulation with $$N$$ nodes is then$$ (1 - P(\text{failure}))^N $$.  This scales terribly with the failure rate, so in practice we divide simulations up into shorter simulations that resume where the prior simulation left off to keep $$ P(\text{failure}) $$ low enough, and to not lose days of simulation time when a crash occurs.

In general, the ACID properties are difficult to write for all the ways you can build data structures in a computer - so we need to find a way to bring structure to data so we can achieve these.

## Relational Algebra

At this point, there are still many choices of relational databases based on relational algebra, which is a set of rules that allow for query languages (like SQL) to be constructed.  These rules are similar to basic set theory in mathematics, and define how you interact with data with set union, difference, cartesian products etc.  This then gets translated into userland jargon into a query language, which inexplicably to me SQL has market leading inertia.
Again, these are pretty old ideas, and in fact were meant to bring order to the chaos of preceeding data systems, some of which were graph databases.  Old is new again, etc.  Maybe since so many SQL users learn by doing, at least around here more people should probably read ["A relational Model of Data for Large Shared Data Banks" (Cobb 1970)"](https://doi.org/10.1145/362384.362685).











Increasingly, graph database systems seem to be becoming trendy.  Or so it would seem.  
