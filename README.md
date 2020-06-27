# Life graph

Inspired by [this post](https://waitbutwhy.com/2014/05/life-weeks.html), I decided I wanted to make my own graph of my life.
In the comments on that post, there are many other graphs available, but most of them add lots of different things that I did
not care for. They looked extremely nice, but not nearly as simple as the box of squares originally showed in the post. The simplicity
of seeing my life on a tiny grid really hit me. I wanted to recreate that.

The folks at [waitbutwhy.com](https://waitbutwhy.com) own the idea behind this work. They gave me permission to produce and realease
this code for free use by everyone else.

# A Simple Grid
To make a grid of squares, this is all you need.
```
birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=90)
g.save("examples/images/grid.png")
```
![A simple grid][grid]

[grid]: https://github.com/K20shores/Life-Graph/blob/master/examples/images/grid.png "A Simple Grid"