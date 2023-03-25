import unittest
import matplotlib.pyplot as plt
from datetime import date

from lifegraph.lifegraph import Lifegraph, Side

class TestLifeGraph(unittest.TestCase):

    def test_save(self):
        birthday = date(1990, 11, 1)
        g = Lifegraph(birthday, max_age=100)

        # uses a random color
        g.add_life_event('My first paycheck', date(2006, 8, 23))

        # specify color with hex string
        g.add_life_event('Graduated\nhighschool', date(2008, 6, 2), color="#00FF00", side=Side.LEFT)

        # specify color with RGB
        g.add_life_event('First car purchased', date(2010, 7, 14), color = (1, 0, 0))

        path = "images/grid_life_event.png"
        g.save(path)

        plt.imread(path) # Raises FileNotFoundError if file not found
        # Check that the file is not empty
        with open(path, 'rb') as f:
            self.assertGreater(len(f.read()), 0)

if __name__ == '__main__':
    unittest.main()