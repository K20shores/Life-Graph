import unittest

import matplotlib.pyplot as plt
import numpy as np

from datetime import date
from lifegraph.lifegraph import Lifegraph, Side

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
        path = "images/grid_life_event.png"
        g.save(path)
        # TODO: add a check for this

    def test_rc_params(self):
        birthday = date(1990, 11, 1)
        rcParams = {}
        rcParams["lines.marker"] = 'v'
        rcParams["lines.markersize"] = 2.0

        g = Lifegraph(birthday, max_age=100, rcParams=rcParams)
        g.save("images/grid_customization.png")
        # TODO: add a check for this

if __name__ == '__main__':
    unittest.main()