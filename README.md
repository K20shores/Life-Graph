<!-- Images -->
[alife]: examples/images/alife.png "A Life Graph"
[grid]: examples/images/grid.png "A Simple Grid"
[grid_with_title]: examples/images/grid_with_title.png "With a Title"
[grid_with_watermark]: examples/images/grid_with_watermark.png "With a Watermark"
[grid_maxage]: examples/images/grid_maxage.png "With a Watermark"
[grid_life_event]: examples/images/grid_life_event.png "With a Watermark"

# Life Graph
Inspired by [this post](https://waitbutwhy.com/2014/05/life-weeks.html), I decided I wanted to make my own graph of my life.
In the comments on that post, there are many other graphs available, but most of them add lots of different things that I did
not care for. They looked extremely nice, but not nearly as simple as the box of squares originally showed in the post. The simplicity
of seeing my life on a tiny grid really hit me. I wanted to recreate that.

The folks at [waitbutwhy.com](https://waitbutwhy.com) own the idea behind this work. They gave me permission to produce and realease
this code for free use by everyone else.

# A Life Graph
![A Life Graph][alife]

# A Simple Grid
To make a grid of squares, this is all you need.
By default, the axes instance is constrained to a smaller portion of the page to make
room for annotations on the edge of the graph. The axes_rect argument ensures that the graph
takes up more room.
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, axes_rect=[.1, .1, .8, .8])
g.save("grid.png")
```

![A simple grid][grid]

# Add a Title
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
g.add_title("Time is Not Equal to Money")
g.save("grid.png")
```

![Adding a title][grid_with_title]

# Add a Watermark
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
g.add_title("Time is Not Equal to Money")
g.add_watermark("Your Life")
g.save("grid.png")
```

![Adding a watermark][grid_with_watermark]

# Display and Change the Max Age
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)
g.add_title("Time is Not Equal to Money")
g.show_max_age_label()
g.save("images/grid_maxage.png")
```

![Changing and displaying the max age][grid_maxage]

# Adding a life event
You can add events of your life. The graph is initialized from your birthday and where
the events are placed on the graph is calculated from your birthdate and the day that 
the event happened. Notice the different ways that you can set the color and that
you can specify which side you'd like to place the text if you don't like the default.

```
from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# a random color will be chosen if you don't provide one
g.add_life_event('My first paycheck', date(2006, 8, 23))

# colors can be added as hex strings
# and you can hint at which side you want the text on
g.add_life_event('Graduated\nhighschool', date(2008, 6, 2), color="#00FF00", side=Side.LEFT)

# or RGB
g.add_life_event('First car purchased', date(2010, 7, 14), color = (1, 0, 0))

g.save("images/grid_life_event.png")
```

![Adding life events][grid_life_event]

# Contributing and Code of Conduct
[Read our contributing guidelines](docs/CONTRIBUTING)

[Read our code of conduct](docs/CODE_OF_CONDUCT.md)