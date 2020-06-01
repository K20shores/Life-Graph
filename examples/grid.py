from lifegraph.lifegraph import Lifegraph, Papersize, random_color, Point, Side
from datetime import date, datetime, timedelta

def main():
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4, max_age=90)

    # g.add_life_event("A Thing", date(2008, 11, 20))
    g.add_life_event("A Thing2", date(2008, 11, 20))
    g.add_life_event("A Much Longer\nThing", date(2008, 11, 20), color='red')
    g.add_life_event("A Much Longer\nThing", date(2008, 8, 20), color='red')

    g.add_era("An Era", date(2018, 11, 20), date(2028, 11, 20))

    g.add_era_span("An Era Span", date(2029, 11, 20), date(2034, 8, 20))

    g.show_max_age_label()
    g.add_title("A Sample Title")

    g.save("examples/grid.png")

main()
