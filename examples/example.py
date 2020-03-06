import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lifegraph.lifegraph import Lifegraph, Papersize, random_color, Point, Side
from datetime import date, datetime

def main():
    print (os.getcwd())
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A2, max_age=90, label_space_epsilon=1)

    g.add_life_event('Married', date(2010, 2, 14), '#DC143C')
    g.add_life_event('Five Years Together', date(2015, 2, 14), '#DC143C')

    #g.add_watermark("Kyle Shores")

    g.add_era("Elementary School", date(1996, 8, 24), date(2002, 6, 5), 'r')
    g.add_era("Intermediate School", date(2002, 8, 24), date(2003, 6, 5), '#00838f')
    g.add_era("Middle School", date(2003, 8, 24), date(2005, 6, 5), 'b')
    g.add_era("High School", date(2005, 8, 24), date(2009, 6, 5), '#00838f')
    g.add_era("College", date(2009, 9, 1), date(2013, 12, 14), (80/255, 0, 0), side=Side.LEFT, font_size=30)

    g.add_era_span("Pregnant with Bilbo Bagginses", date(2016, 1, 22), date(2016, 10, 16), '#D2691E', hint=Point(53, 28))

    g.add_title("Our Life, Together")

    g.add_image("examples/marriage-2260602_1920.jpg", alpha=0.3)

    g.show_max_age_label()

    g.save("examples/lifegraph.png")

main()
