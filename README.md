# Life Graph
[![CI Status](https://github.com/k20shores/Life-Graph/actions/workflows/tests.yml/badge.svg)](https://github.com/k20shores/Life-Graph/actions/workflows/tests.yml)

<!-- Images -->
[alife]: test/images/alife.png "A Life Graph"
[grid]: test/images/grid.png "A Simple Grid"
[grid_with_title]: test/images/grid_with_title.png "With a Title"
[grid_with_watermark]: test/images/grid_with_watermark.png "With a Watermark"
[grid_maxage]: test/images/grid_maxage.png "Adding the max age"
[grid_life_event]: test/images/grid_life_event.png "A life event"
[grid_era]: test/images/grid_era.png "An era"
[grid_era_span]: test/images/grid_era_span.png "An era span"
[grid_add_image]: test/images/grid_add_image.png "Add an image"
[grid_customization]: test/images/grid_customization.png "Customize the grid"
[annotation_placement]: test/images/placement.png "Annotation placement"

# Life Graph Inspiration
Inspired by [this post](https://waitbutwhy.com/2014/05/life-weeks.html), I decided I wanted to make my own graph of my life.
In the comments on that post, there are many other graphs available, but most of them add lots of different things that I did
not care for. They looked extremely nice, but not nearly as simple as the box of squares originally showed in the post. The simplicity
of seeing my life on a tiny grid really hit me. I wanted to recreate that.

The folks at [waitbutwhy.com](https://waitbutwhy.com) own the idea behind this work. They gave me permission to produce and realease
this code for free use by everyone else.

# A Life Graph Example
https://github.com/K20shores/Life-Graph/blob/69cd0d1e6fb4f5ade2eb71ca1c6b2f1fb5955337/test/tests.py#L88-L111
![A Life Graph][alife]

# A Simple Grid
To make a grid of squares, this is all you need.
By default, the axes instance is constrained to a smaller portion of the page to make
room for annotations on the edge of the graph. The axes_rect argument ensures that the graph
takes up more room.

https://github.com/K20shores/Life-Graph/blob/bc3da6d79342d6bf5b04263d0a136f05d016fd4f/test/tests.py#L22-L24
![A simple grid][grid]

# Add a Title
https://github.com/K20shores/Life-Graph/blob/56e685f500919b9570ca95998c0dad284fd046df/test/tests.py#L29-L33
![Adding a title][grid_with_title]

# Add a Watermark
https://github.com/K20shores/Life-Graph/blob/56e685f500919b9570ca95998c0dad284fd046df/test/tests.py#L43-L46
![Adding a watermark][grid_with_watermark]

# Display and Change the Max Age
https://github.com/K20shores/Life-Graph/blob/56e685f500919b9570ca95998c0dad284fd046df/test/tests.py#L36-L39
![Changing and displaying the max age][grid_maxage]

# Adding a Life Event
You can add events of your life. The graph is initialized from your birthday and where
the events are placed on the graph is calculated from your birthdate and the day that 
the event happened. Notice the different ways that you can set the color and that
you can specify which side you'd like to place the text if you don't like the default.


![Adding life events][grid_life_event]

# Adding an Era
You can color parts of your life that marked an era.
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# random color will be used
g.add_era('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))

# you can also choose the color
g.add_era('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")

g.save("images/grid_era_span.png")
```

![Adding eras][grid_era]

# Adding an Era Span
Or you can use this dumbbell shape to denote eras
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# random color will be used
g.add_era_span('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))

# you can also choose the color
g.add_era_span('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")

g.save("images/grid_era_span.png")
```

![Adding era spans][grid_era_span]

# Add an Image
You can add images to the axes instance.
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

g.add_image("couple.jpg", alpha=0.5)

g.save("images/grid_add_image.png")
```
![Adding an image][grid_add_image]

# Customize the Grid
The grid properties for each papersize is controlled by the matplotlib rc paramters. The paramters
for each papersize can be found in [the configuration file](lifegraph/configuration.py).
```
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

g.settings.rcParams["lines.marker"] = 'v'
g.settings.rcParams["lines.markersize"] = 2.0

g.save("images/grid_customization.png")
```

There are a number of other rc parameters defined for this package. There are really
too many to provide an example of each. Please see the availabel 
configurations for a better idea of what can be customized. Some of the 
customizable parameters can be set with the lifegraph. For example, `g.format_x_axis(positionx=0, positiony=0)` is equivalent to `g.settings.otherParams['xlabel.position'] = (0, 0)` (both coordinates are in axes coordinates) and would move the 'Week of the year ->' text to the bottom left of the graph.

![Customizing the grid][grid_customization]

# Annotation Placement

By default, the graph will place annotations from top to bottom. The graph lays out annotations
so that they do not overlap. If annotations do overlap, this is a bug. Please file a bug report. Annotations
for events in the first 26 weeks of a year in your life will be on the right side, everything else on the left.

However, you can control the placement if you wish through the use of the `hint` and `side` keyword arguments.

```
from lifegraph.lifegraph import Lifegraph, Papersize, Side
from datetime import date

birthday = date(1990, 11, 1)
g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100)

g.add_title("Time is Not Equal to Money")
g.show_max_age_label()

# the default placement
g.add_life_event('My first paycheck', date(2006, 1, 23), color='r')

# a hint, in data coordinates
g.add_life_event('My first paycheck', date(2006, 1, 23), color='r', hint=(10, -10))

# a side
g.add_life_event('My first paycheck', date(2006, 1, 23), color='r', side=Side.RIGHT)

# the default placement
g.add_era_span('Green thing', start_date=date(2010, 2, 1), end_date=date(2011, 8, 1), color='g')

# a hint, in data coordinates
g.add_era_span('Red thing', start_date=date(2012, 2, 1), end_date=date(2013, 8, 1), color='r', hint=(52, 105))

# a side
g.add_era_span('Blue thing', start_date=date(2014, 2, 1), end_date=date(2015, 8, 1), color='b', side=Side.LEFT)

g.save("images/placement.png")
```

![Annotation Placement][annotation_placement]

# Contributing and Code of Conduct
[Read our contributing guidelines](docs/CONTRIBUTING)

[Read our code of conduct](docs/CODE_OF_CONDUCT.md)