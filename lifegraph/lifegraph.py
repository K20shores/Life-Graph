import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import numpy as np
import datetime
import random
import logging

from matplotlib.transforms import Bbox
from matplotlib import colors as mcolors
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum

logging.basicConfig(filename='app.log', filemode='a',
                    format='[%(asctime)s-%(name)s] [%(levelname)s] %(message)s', level=logging.INFO)

exclude = []
colors = [(key, val)
          for key, val in mcolors.BASE_COLORS.items() if val not in exclude]
for key, val in mcolors.CSS4_COLORS.items():
    if val not in exclude:
        colors.append((key, val))


def random_color():
    """Returns a random color defined in matplotlib.colors.BASE_COLORS or matpotlib.colors.CSS4_COLORS"""
    c = colors[random.randint(0, len(colors) - 1)]
    return c[1]


class Side(Enum):
    """Visually indicates the left or right of the plot"""
    LEFT = 1
    RIGHT = 2


class Point:
    """A point class that holds the x and y coordinates in data units"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


class DatePosition(Point):
    """A class to hold the week, year of life, and date assocaited with a Point"""

    def __init__(self, x, y, week, year_of_life, date):
        super().__init__(x, y)
        self.week = week
        self.year_of_life = year_of_life
        self.date = date

    def __repr__(self):
        return f"DatePosition: year({self.year_of_life}), week({self.week}), date({self.date}) at point {super().__repr__()}"

    def __str__(self):
        return f"DatePosition: year({self.year_of_life}), week({self.week}), date({self.date}) at point {super().__repr__()}"


class Marker(Point):
    """A class to indicate how and where to draw a marker"""

    def __init__(self, x, y, marker='s', fillstyle='none', color='black'):
        super().__init__(x, y)
        self.marker = marker
        self.fillstyle = fillstyle
        self.color = color

    def __repr__(self):
        return f"Marker at {super().__repr__()}"

    def __str__(self):
        return f"Marker at {super().__repr__()}"


class Annotation(Point):
    """A class to hold the text of an annotation with methods to help layout the text."""
    # the default for marker size is 10.0, which should be the default for matplotlib text objects

    def __init__(self, date, text, label_point, marker='s', color='black', bbox=None, event_point=None, font_size=10.0, draw_point=True, shrink=0):
        super().__init__(label_point.x, label_point.y)
        self.date = date
        self.text = text
        self.marker = marker
        self.color = color
        self.bbox = bbox
        self.event_point = event_point
        self.font_size = font_size
        self.draw_point = draw_point
        self.shrink = shrink

    def set_metadata(self, bbox):
        """Set the bounding box of an annotation

        :param bbox: a matplotlib.transforms.Bbox instance

        """
        self.bbox = bbox

    def overlaps(self, that):
        """Check that the two Bboxes don't overlap
        
        They don't overlap if
            1) one rectangle's left side is strictly to the right other's right side
            2) one rectangle's top side is stricly bellow the other's bottom side

        :param that: an Annotation

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")

        if (self.bbox.x0 >= that.bbox.x1 or that.bbox.x0 >= self.bbox.x1):
            return False

        # the coordinates are inverted, so y0 is larger than y1
        if (self.bbox.y0 <= that.bbox.y1 or that.bbox.y0 <= self.bbox.y1):
            return False

        return True

    def is_within_epsilong_of(self, that, epsilon):
        """Check that the two Bboxes don't overlap
        
        They don't overlap if
            1) one rectangle's left side is strictly to the right other's right side
            2) one rectangle's top side is stricly bellow the other's bottom side

        :param that: An Annotation
        :param epsilon: A real number to define the tolerance for how close the label text can be

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")

        if (self.bbox.x0 + epsilon >= that.bbox.x1 or that.bbox.x0 + epsilon >= self.bbox.x1):
            return False

        # the coordinates are inverted, so y0 is larger than y1
        if (self.bbox.y0 + epsilon <= that.bbox.y1 or that.bbox.y0 + epsilon <= self.bbox.y1):
            return False

        return True

    def xy_overlapping_width_height(self, that, epsilon):
        """Detmerine by how much the two annotation bounding boxes overlap

        :param that: an Annotation
        :param epsilon: A real number that will add a buffer space between the two label text bounding boxes

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")

        # find the width and height of the overlapping rectangle
        width = min(self.bbox.x1, that.bbox.x1) - \
            max(self.bbox.x0, that.bbox.x0)
        # the coordinates are inverted, so y0 is larger than y1
        height = min(self.bbox.y0, that.bbox.y0) - \
            max(self.bbox.y1, that.bbox.y1)
        return (width + epsilon, height + epsilon)

    def update_X_with_correction(self, correction):
        """Move the label text in the x direction according to the value in correction

        :param correction: a tuple of real number where correction[0] determines by how much the x position of the label should move

        """
        self.x += correction[0]
        self.bbox.x0 += correction[0]
        self.bbox.x1 += correction[0]

    def update_Y_with_correction(self, correction):
        """Move the label text in the y direction according to the value in correction

        :param correction: a tuple of real number where correction[1] determines by how much the y position of the label should move

        """
        self.y += correction[1]
        self.bbox.y0 += correction[1]
        self.bbox.y1 += correction[1]

    def __repr__(self):
        return f"Annotation '{self.text}' at {super().__repr__()}"

    def __str__(self):
        return f"Annotation '{self.text}' at {super().__repr__()}"


class Era():
    """A class which shows a highlighted area on the graph to indicate a span of time"""

    def __init__(self, text, start, end, color):
        self.text = text
        self.start = start
        self.end = end
        self.color = color

    def __repr__(self):
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"

    def __str__(self):
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"


class Papersize:
    """A class holding papersize in inches"""
    # all sizes are in inches
    _4A0 = [66.2, 93.6]
    _2A0 = [46.8, 66.2]
    A0 = [33.1, 46.8]
    A1 = [23.4, 33.1]
    A2 = [16.5, 23.4]
    A3 = [11.7, 16.5]
    A4 = [8.3, 11.7]
    A5 = [5.8, 8.3]
    A6 = [4.1, 5.8]
    A7 = [2.9, 4.1]
    A8 = [2.0, 2.9]
    A9 = [1.5, 2.0]
    A10 = [1.0, 1.5]
    HalfLetter = [5.5, 8.5]
    Letter = [8.5, 11.0]
    Legal = [8.5, 14.0]
    JuniorLegal = [5.0, 8.0]
    Ledger = [11.0, 17.0]
    Tabloid = [11.0, 17.0]


class Lifegraph:
    """This class will represent your life as a graph of boxes"""

    def __init__(self, birthdate, size=Papersize.A3, dpi=300, label_space_epsilon=.2, show_watermark=False):
        logging.info(f"Initializing lifegraph")
        if birthdate is None or not isinstance(birthdate, datetime.date):
            raise ValueError("birthdate must be a valid datetime.date object")

        self.birthdate = birthdate

        # figure size and resolution
        self.size = size
        self.dpi = dpi
        self.fig = plt.figure(figsize=self.size, dpi=self.dpi)
        self.ax = self.fig.add_subplot()
        self.renderer = None

        # the data limits, we want a grid of 52 weeks by 90 years
        # negative minimum so that ths squares are not cut off
        self.xmin = -.5
        self.xmax = 52
        self.ymin = -.5
        self.ymax = 90

        self.xlims = [self.xmin, self.xmax]
        self.ylims = [self.ymin, self.ymax]

        self.data = []

        # drawing controls
        self.inner_padx = -4
        self.inner_pady = -4
        self.color = 'black'
        self.marker = 's'
        self.fillstyle = 'none'
        self.linestyle = 'none'
        self.grid_mew = .5
        self.left_annotation_offset = 3
        self.right_annotation_offset = 3
        self.annotation_marker_size = 12
        self.annotation_edge_width = 1.5

        self.show_watermark = show_watermark
        self.watermark_text = ''

        self.fontsize = 25

        self.era_offset = .5
        self.era_linewidth = 10.0
        self.era_alpha = 0.2
        self.era_shrink = 10

        self.label_space_epsilon = label_space_epsilon

        self.annotations_left = []
        self.annotations_right = []
        self.eras = []
        self.era_spans = []

    def add_90(self):
        """Places the text '90' on the bottom right of the plot"""
        ax2 = self.ax.twinx()
        ax2.set_yticklabels(
            [90], fontdict={'fontweight': 'bold', 'fontsize': 20})
        ax2.yaxis.set_tick_params(width=0)
        ax2.set_frame_on(False)

    def add_life_event(self, text, date, color, hint=None, side=None):
        """

        :param text: param date:
        :param color: param hint:  (Default value = None)
        :param side: Default value = None)
        :param date: 
        :param hint:  (Default value = None)

        """
        logging.info(f"Adding life event '{text}' with color {color}")
        if (date < self.birthdate or date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (hint is not None and side is not None):
            raise ValueError(
                f"Hint and side are mutually exclusive arguments. Specify only one of them.")

        week = int(np.floor((date - self.birthdate).days / 7)) + 1
        x = week % self.xmax
        y = int(np.floor(week / self.xmax))

        hint = self.__sanitize_hint(hint)
        self.data.append(Marker(x, y, color=color))

        labelx = self.xmax if (x > self.xmax / 2) else 0
        labely = y

        if hint is not None:
            lablex = hint.x
            labely = hint.y

        if side is not None:
            if side == Side.LEFT:
                labelx = 0
            else:
                labelx = self.xmax

        label_point = Point(labelx, labely)

        a = Annotation(date, text, label_point=label_point, color=color,
                       event_point=Point(x, y), shrink=self.annotation_marker_size / 2)
        if (labelx > self.xmax / 2):
            self.annotations_right.append(a)
        else:
            self.annotations_left.append(a)

    def add_era(self, text, start_date, end_date, color, hint=None, side=None):
        """

        :param text: param start_date:
        :param end_date: param color:
        :param hint: Default value = None)
        :param side: Default value = None)
        :param start_date: 
        :param color: 

        """
        logging.info(f"Adding era '{text}' with color {color}")
        if (start_date < self.birthdate or start_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (end_date < self.birthdate or end_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (hint is not None and side is not None):
            raise ValueError(
                f"Hint and side are mutually exclusive arguments. Specify only one of them.")

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)

        self.eras.append(Era(text, start_position, end_position, color))

        label_point = self.__get_label_point(hint, side, start_position, end_position)
        # when sorting the annotatio the date is used
        # choose the middle date so that the annotation ends up
        # as close to the middle of the era as possible
        # if no hint was provided
        middle_date = start_date + (end_date - start_date)/2

        a = Annotation(middle_date, text, label_point=label_point, color=color,
                       event_point=label_point, font_size=20.0, draw_point=False, shrink=self.era_shrink)
        if (label_point.x > self.xmax / 2):
            self.annotations_right.append(a)
        else:
            self.annotations_left.append(a)

    def add_era_span(self, text, start_date, end_date, color='g', hint=None, side=None):
        """

        :param text: param start_date:
        :param end_date: param color:  (Default value = 'g')
        :param hint: Default value = None)
        :param side: Default value = None)
        :param start_date: 
        :param color:  (Default value = 'g')

        """
        logging.info(f"Adding era span '{text}' with color {color}")
        if (start_date < self.birthdate or start_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (end_date < self.birthdate or end_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (hint is not None and side is not None):
            raise ValueError(
                f"Hint and side are mutually exclusive arguments. Specify only one of them.")

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)
        label_point = self.__get_label_point(hint, side, start_position, end_position)

        # this will put a dumbbell onto the graph spanning the era
        self.era_spans.append(Era(text, start_position, end_position, color))

        middle_date = start_date + (end_date - start_date)/2

        middle_of_line_x = np.average((start_position.x, end_position.x))
        middle_of_line_y = np.average((start_position.y, end_position.y))
        event_point = Point(middle_of_line_x, middle_of_line_y)

        self.annotations_right.append(Annotation(middle_date, text, label_point=label_point,
                                                 color=color, event_point=event_point, font_size=20.0, draw_point=False))

    def add_watermark(self, text):
        """

        :param text: 

        """
        self.watermark_text = text
        self.show_watermark = True

    def show(self):
        """ """
        self.ax.show()

    def close(self):
        """ """
        self.ax.close()

    def save(self, name, transparent=False):
        """

        :param name: param transparent:  (Default value = False)
        :param transparent:  (Default value = False)

        """
        logging.info(f"Saving lifegraph with name {name}.")
        self.__draw()
        plt.savefig(name, transparent=transparent, bbox_inches="tight")

    def __draw(self):
        """ """
        plt.rc('text', usetex=True)
        xs = np.arange(1, self.xmax+1)
        ys = [np.arange(0, self.ymax) for i in range(self.xmax)]

        self.ax.plot(xs, ys, color=self.color, marker=self.marker,
                     fillstyle=self.fillstyle, linestyle='none', mew=self.grid_mew)

        for point in self.data:
            self.ax.plot(point.x, point.y, color=point.color, marker=point.marker,
                         fillstyle=point.fillstyle, linestyle='none', mew=self.grid_mew)

        self.__format_xaxis()
        self.__format_yaxis()

        self.__draw_annotations()
        self.__draw_eras()
        self.__draw_era_spans()
        self.__draw_watermark()

        # hide the horizontal and vertical lines
        self.ax.set_frame_on(False)

        self.ax.set_aspect('equal', adjustable='box')

    def __format_xaxis(self):
        """ """
        self.ax.set_xlim(self.xlims)
        # put x ticks on top
        xticks = [1]
        xticks.extend(range(5, self.xmax+5, 5))
        self.ax.xaxis.tick_top()
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticks[:-1])
        self.ax.set_xlabel(r'Week of the Year $\longrightarrow$',
                           color='blue', fontsize=self.fontsize)
        self.ax.xaxis.set_label_position('top')
        self.ax.xaxis.set_label_coords(0.35, 1.02)
        self.ax.xaxis.set_tick_params(
            width=0, direction='out', pad=self.inner_padx)

    def __format_yaxis(self):
        """ """
        self.ax.set_ylim(self.ylims)
        # set y ticks
        yticks = [*range(0, self.ymax, 5)]
        self.ax.set_yticks(yticks)
        self.ax.set_ylabel(r'$\longleftarrow$ Age',
                           color='blue', fontsize=self.fontsize)
        self.ax.yaxis.set_label_coords(-0.02, 0.90)
        self.ax.yaxis.set_tick_params(
            width=0, direction='in', pad=self.inner_pady)
        self.ax.invert_yaxis()

    def __draw_annotations(self):
        """ """
        final = []
        final.extend(self.__resolve_annotations(
            self.annotations_left, Side.LEFT))
        final.extend(self.__resolve_annotations(
            self.annotations_right, Side.RIGHT))

        for a in final:
            if a.draw_point:
                self.ax.plot(a.event_point.x, a.event_point.y, marker='o', color=a.color,
                             markerfacecolor='none', ms=self.annotation_marker_size, mew=self.annotation_edge_width)
            self.ax.annotate(a.text, xy=(a.event_point.x, a.event_point.y), xytext=(a.x, a.y),
                             weight='bold', color=a.color, size=a.font_size, va='center_baseline',
                             arrowprops=dict(arrowstyle='-',
                                             connectionstyle="arc3",
                                             color=a.color,
                                             shrinkB=a.shrink))

    def __draw_eras(self):
        """ """
        xmin = self.ax.transLimits.transform((1-.5, 0))[0]
        xmax = self.ax.transLimits.transform((self.xmax+.5, 0))[0]
        for era in self.eras:
            for y in range(era.start.y, era.end.y+1):
                if y == era.start.y:
                    axesUnits = self.ax.transLimits.transform(
                        (era.start.x-.5, era.start.y))
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=self.era_alpha, xmin=axesUnits[0], xmax=xmax)
                elif y == era.end.y:
                    axesUnits = self.ax.transLimits.transform(
                        (era.end.x+.5, era.end.y))
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=self.era_alpha, xmin=xmin, xmax=axesUnits[0])
                else:
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=self.era_alpha, xmin=xmin, xmax=xmax)

    def __draw_era_spans(self):
        """ """
        for era in self.era_spans:
            radius = .5
            circle1 = plt.Circle((era.start.x, era.start.y), radius,
                                 color=era.color, fill=False, lw=self.annotation_edge_width)
            circle2 = plt.Circle((era.end.x, era.end.y), radius,
                                 color=era.color, fill=False, lw=self.annotation_edge_width)
            self.ax.add_artist(circle1)
            self.ax.add_artist(circle2)

            # to draw the line between the two circles, we need to find the point on the
            # each circle that is closest to the other circle
            # get the angle from one circle to the other and find the point on the circle
            # that lies at that angle
            x1 = era.end.x - era.start.x
            y1 = era.end.y - era.start.y

            x2 = era.start.x - era.end.x
            y2 = era.start.y - era.end.y

            # quadrant senstive arctan
            angle1 = np.arctan2(y1, x1)
            angle2 = np.arctan2(y2, x2)

            x1 = era.start.x + np.cos(angle1) * radius
            y1 = era.start.y + np.sin(angle1) * radius

            x2 = era.end.x + np.cos(angle2) * radius
            y2 = era.end.y + np.sin(angle2) * radius

            l = mlines.Line2D([x1, x2], [y1, y2], color=era.color)
            self.ax.add_line(l)

    def __draw_watermark(self):
        """ """
        if self.show_watermark:
            self.fig.text(0.5, 0.5, self.watermark_text,
                          fontsize=100, color='gray',
                          ha='center', va='center', alpha=0.3, rotation=65, transform=self.ax.transAxes)

    def __resolve_annotations(self, annotations, side):
        """

        :param annotations: 
        :param side: 

        """
        for a in annotations:
            # first, get the bounds
            self.__set_annotation_metadata(a)

            # now set the intitial positions
            # we want all of the text to be on the left or right of the squares
            width = a.bbox.width
            x = 0
            if side == side.LEFT:
                x = self.xmin - self.left_annotation_offset - width
            else:
                x = self.xmax + self.right_annotation_offset
            a.x = x
            a.bbox.x0 = x
            a.bbox.x1 = x + width

        annotations.sort(key=lambda a: a.date)
        final = []
        for unchecked in annotations:
            for checked in final:
                if unchecked.overlaps(checked):
                    correction = unchecked.xy_overlapping_width_height(
                        checked, self.label_space_epsilon)
                    unchecked.update_Y_with_correction(correction)
                if unchecked.is_within_epsilong_of(checked, self.label_space_epsilon):
                    correction = [0, self.label_space_epsilon]
                    unchecked.update_Y_with_correction(correction)
            final.append(unchecked)

        return final

    def __to_date_position(self, date):
        week = int(np.floor((date - self.birthdate).days / 7)) + 1
        x = week % self.xmax
        y = int(np.floor(week / self.xmax))
        year_of_life = y
        return DatePosition(x, y, week, year_of_life, date)

    def __sanitize_hint(self, hint):
        """ Hints should have an x value < 0 or bigger than self.xmax
        """
        # TODO: what should this be?
        edge = 10
        if hint is not None:
            if (hint.x >= self.xmax / 2 and hint.x < self.xmax) or hint.x > self.xmax + edge:
                hint.x = self.xmax
            if hint.x > 0 <= self.xmax / 2 or hint.x < -edge:
                hint.x = 0

        return hint

    def __set_annotation_metadata(self, a):
        """

        :param a: 

        """
        # put the text on the plot temporarily so that we can determine the width of the text
        t = self.ax.text(a.x, a.y, a.text, transform=self.ax.transData,
                         ha='center', va='center', size=a.font_size)

        if (self.renderer is None):
            self.renderer = self.fig.canvas.get_renderer()

        # in display units
        bbox = t.get_window_extent(renderer=self.renderer)
        # now convert it to data units
        bbox_data_units = self.ax.transData.inverted().transform(bbox)
        a.set_metadata(Bbox(bbox_data_units))
        t.remove()

    def __get_label_point(self, hint, side, start_position, end_position):
        hint = self.__sanitize_hint(hint)
        # now add an annotation for the label
        labelx = self.xmax
        labely = np.floor(np.average((start_position.y, end_position.y)))
        if hint is not None:
            labelx = hint.x
            labely = hint.y

        if side is not None:
            if side == Side.LEFT:
                labelx = 0
            else:
                labelx = self.xmax
        
        return Point(labelx, labely)

