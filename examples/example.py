from lifegraph.lifegraph import Lifegraph, Papersize, random_color, Point, Side
from datetime import date, datetime, timedelta

def main():
    birthday = date(1990, 11, 1)

    for sz in Papersize:
        g = Lifegraph(birthday, dpi=600, size=sz, max_age=90, label_space_epsilon=1)

        g.add_life_event('Married', date(2010, 2, 14), '#DC143C')
        g.add_life_event('Five Years\nTogether', date(2015, 2, 14), '#DC143C')

        g.add_watermark("A Person")

        g.add_era("Elementary School", date(1996, 8, 24), date(2002, 6, 5), 'r')
        g.add_era("Intermediate School", date(2002, 8, 24), date(2003, 6, 5), '#00838f')
        g.add_era("Middle School", date(2003, 8, 24), date(2005, 6, 5), 'b')
        g.add_era("High School", date(2005, 8, 24), date(2009, 6, 5), '#00838f')
        g.add_era("College", date(2009, 9, 1), date(2013, 12, 14), (80/255, 0, 0), side=Side.LEFT)

        g.add_era_span("Pregnant with\nBilbo Bagginses", date(2016, 1, 22), date(2016, 10, 16), '#D2691E', hint=Point(54, 28))

        g.add_title("Our Life, Together")

        g.add_image("examples/marriage-2260602_1920.jpg", alpha=0.3)

        g.show_max_age_label()

        g.save(f"examples/lifegraph_{sz.name}.png")

main()
