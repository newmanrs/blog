+++
title = "Cloudburst Brewing Beer and Hops Graph"
date = 2021-06-03
draft = false
categories = ["beer", "hops", "neo4j"]

[[images]]
 src = "/img/cloudburst_beer_graph/azacca.png"
 alt = "Cloudburst beers containing Azacca"
+++

So it came to pass I was at Cloudburst brewing and remarked to another regular that the only way I could remember the beer names and hops within them as well as him would be to scrape the website&hellip; so I did.  And put it into a graph database so I could visualize the networks of related beers and hops.

<!--more-->

The project is still evolving, but the project description and some usage examples are on [github](https://github.com/newmanrs/cloudburst-graph).  I'll be keeping the descriptions there more up to date and a bit more formal about installing and running the project, and with more usage examples and queries.

For now, I'm still working/editing on the project and hopefully will return to revise this post, or create a demonstration Youtube video.

That said, at least one epiphany was that I really enjoyed every Cloudburst beer that contains Azacca, even beers of different styles.  This realization came from viewing the graph of beers containing Azacca hops, and their styles.

![Azacca beers](/img/cloudburst_beer_graph/azacca.png)

Art Deco, That's Baseball Baby, and Show Your Work were all excellent beers, and I probably wouldn't have quite pinned down a connection between them trying to remember years old descriptions or reading through Cloudburst's webpage list and descriptions of several hundred beers.

All the writing I have time for today, hopefully I'll revisit this post soon with some more images and examples.  Scraping the site for beers loading up a database was decent fun, although getting useful hop descriptions by trying to deconstruct PDF files was not.
