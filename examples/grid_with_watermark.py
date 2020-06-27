
from lifegraph.lifegraph import Lifegraph, Papersize
from datetime import date

if __name__ == '__main__':
    birthday = date(1990, 11, 1)
    g = Lifegraph(birthday, dpi=300, size=Papersize.A4)
    g.add_title("Time is Not Equal to Money")
    g.add_watermark("Your Life")
    g.save("images/grid_with_watermark.png")
