import unittest

import matplotlib.pyplot as plt
import numpy as np
import datetime

from datetime import date, datetime
from datetime import date
from lifegraph.lifegraph import Lifegraph, Side, Point

class TestLifeGraph(unittest.TestCase):

    def test_save(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, axes_rect=[.1, .1, .8, .8])
        path = "images/grid.png"
        g.save(path)
        plt.imread(path) # Raises FileNotFoundError if file not found
        # Check that the file is not empty
        with open(path, 'rb') as f:
            self.assertGreater(len(f.read()), 0)

    def test_grid(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, axes_rect=[.1, .1, .8, .8])
        g.save("images/grid.png")

    def test_grid_with_title(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday)
        g.add_title("Time is Not Equal to Money")
        g.save("images/grid_with_title.png")
        self.assertEqual(g._last_title, "Time is Not Equal to Money")

    def test_grid_with_max_age(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, max_age=100)
        g.add_title("Time is Not Equal to Money")
        g.save("images/grid_with_max_age.png")
        self.assertEqual(g.ax.get_ylim()[0], 100)

    def test_grid_with_watermark(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday)
        g.add_watermark("Your Life")
        g.save("images/grid_with_watermark.png")
        text_objs = g.fig.findobj(lambda obj: isinstance(obj, plt.Text))
        has_watermark = [i.get_text() == "Your Life" for i in text_objs]
        self.assertTrue(np.any(has_watermark))

    def test_era(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday)
        g.add_era('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))
        g.add_era('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")
        g.save("images/grid_era.png")
        # TODO: add a check for this

    def test_era_span(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday)
        g.add_era_span('That one thing\nI did as a kid', date(2000, 3, 4), date(2005, 8, 22))
        g.add_era_span('Running for city\ncouncil', date(2019, 12, 10), date(2020, 11, 5), color="#4423fe")
        g.save("images/grid_era_span.png")
        # TODO: add a check for this

    def test_life_event(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, max_age=100)
        g.add_life_event('My first paycheck', date(2006, 8, 23))
        g.add_life_event('Graduated\nhighschool', date(2008, 6, 2), color="#00FF00", side=Side.LEFT)
        g.add_life_event('First car purchased', date(2010, 7, 14), color = (1, 0, 0))
        g.save("images/grid_life_event.png")
        # TODO: add a check for this

    def test_rc_params(self):
        birthday = date(1990, 11, 1)
        rcParams = {}
        rcParams["lines.marker"] = 'v'
        rcParams["lines.markersize"] = 2.0

        g = Lifegraph(birthday, max_age=100, rcParams=rcParams)
        g.save("images/grid_customization.png")
        # TODO: add a check for this

    def test_a_life(self):
        birthday = date(1995, 11, 20)
        g = Lifegraph(birthday, label_space_epsilon=1)

        g.add_life_event('Won an award', date(2013, 11, 20), '#014421')
        g.add_life_event('Hiked the Rocky Mountains', date(2014, 2, 14), '#DC143C', hint=(25, -3))
        g.add_life_event('Ran first marathon', date(2017, 9, 11), '#990000')
        g.add_life_event('Built a canoe', date(2018, 12, 8), '#87CEFA')
        g.add_life_event('Started working at\nEcosia', date(2019, 1, 7), '#00008B')

        now = datetime.utcnow()
        g.add_life_event('Today', date(now.year, now.month, now.day), (0.75, 0, 0.75))

        g.add_era("Elementary School", date(2001, 8, 24), date(2007, 6, 5), 'r')
        g.add_era("Intermediate School", date(2007, 8, 24), date(2008, 6, 5), '#00838f')
        g.add_era("Middle School", date(2008, 8, 24), date(2010, 6, 5), 'b')
        g.add_era("High School", date(2010, 8, 24), date(2014, 6, 5), '#00838f')
        g.add_era("College", date(2014, 9, 1), date(2018, 12, 14), (80/255, 0, 0), side=Side.LEFT)

        g.add_era_span("Longest vacation ever", date(2016, 8, 22), date(2016, 12, 16), '#D2691E', hint=Point(53, 28))

        g.add_title("The life of Someone")

        g.show_max_age_label()
        g.save("images/alife.png")

    def test_placement(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, max_age=100)

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
        # TODO: add a check for this

    def test_add_image(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, max_age=100)
        g.add_image("couple.jpg", alpha=0.5)
        g.save("images/grid_add_image.png")
        # TODO: add a check for this

    def test_can_provide_axis(self):
        birthday = date(1990, 11, 1)
        fig, ax = plt.subplots(dpi=300)
        g = Lifegraph(birthday, ax=ax, max_age=100)
        g.save("images/axis_provided.png")
        # TODO: add a check for this

if __name__ == '__main__':
    unittest.main()