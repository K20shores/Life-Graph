from lifegraph.lifegraph import Lifegraph, Papersize, random_color, Point, Side
from datetime import date, datetime

def main():
    birthday = date(1995, 11, 20)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=100, label_space_epsilon=1)

    g.settings.otherParams["annotation.left.offset"] = 3
    g.settings.otherParams["annotation.right.offset"] = 3

    # same day that I was accepted onto performance team :`)
    g.add_life_event('thing 1', date(2017, 9, 11), '#990000')
    g.add_life_event('thing 2', date(2019, 1, 7), '#00008B')
    g.add_life_event('thing 3', date(2018, 12, 8), '#87CEFA')
    g.add_life_event('thing 4', date(2013, 11, 20), '#014421')
    g.add_life_event('thing 5', date(2014, 2, 14), '#DC143C', hint=(25, -5))
    g.add_life_event(r'thing 6', date(2020, 2, 14), (.522, .733, .396))

    now = date(2020, 8, 22)
    g.add_life_event('Today', date(now.year, now.month, now.day), (0.75, 0, 0.75))

    g.add_era("thing 7", date(2001, 8, 24), date(2007, 6, 5), 'r')
    g.add_era("thing 8", date(2007, 8, 24), date(2008, 6, 5), '#00838f')
    g.add_era("thing 9", date(2008, 8, 24), date(2010, 6, 5), 'b')
    g.add_era("thing 10", date(2010, 8, 24), date(2014, 6, 5), '#00838f')
    g.add_era("thing 11", date(2014, 9, 1), date(2018, 12, 14), (80/255, 0, 0), side=Side.LEFT)

    g.add_era_span("thing 12", date(2016, 8, 22), date(2016, 12, 16), '#D2691E', hint=Point(53, 28))

    g.add_title("Title")

    g.show_max_age_label()

    g.save("images/hint_collision.png")

main()
