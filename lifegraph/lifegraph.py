import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import matplotlib.image as mpimg
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
        """

        :param x: 
        :param y: 

        """
        self.x = x
        self.y = y

    def __repr__(self):
        """ """
        return f"({self.x}, {self.y})"

    def __str__(self):
        """ """
        return f"({self.x}, {self.y})"


class DatePosition(Point):
    """A class to hold the week, year of life, and date assocaited with a Point"""

    def __init__(self, x, y, week, year_of_life, date):
        """

        :param x: 
        :param y: 
        :param week: 
        :param year_of_life: 
        :param date: 

        """
        super().__init__(x, y)
        self.week = week
        self.year_of_life = year_of_life
        self.date = date

    def __repr__(self):
        """ """
        return f"DatePosition: year({self.year_of_life}), week({self.week}), date({self.date}) at point {super().__repr__()}"

    def __str__(self):
        """ """
        return f"DatePosition: year({self.year_of_life}), week({self.week}), date({self.date}) at point {super().__repr__()}"


class Marker(Point):
    """A class to indicate how and where to draw a marker"""

    def __init__(self, x, y, marker='s', fillstyle='none', color='black'):
        """

        :param x: The x position of a marker
        :param y: The y position of a marker
        :param marker:  (Default value = 's')
        :param fillstyle:  (Default value = 'none')
        :param color:  (Default value = 'black')

        """
        super().__init__(x, y)
        self.marker = marker
        self.fillstyle = fillstyle
        self.color = color

    def __repr__(self):
        """ """
        return f"Marker at {super().__repr__()}"

    def __str__(self):
        """ """
        return f"Marker at {super().__repr__()}"


class Annotation(Point):
    """A class to hold the text of an annotation with methods to help layout the text."""

    def __init__(self, date, text, label_point, color='black', bbox=None, event_point=None, font_size=10.0, put_circle_around_point=True, shrink=0, marker=None, relpos=(.5, .5)):
        """

        :param date: 
        :param text: 
        :param label_point: 
        :param color:  (Default value = 'black')
        :param bbox:  (Default value = None)
        :param event_point:  (Default value = None)
        :param font_size:  (Default value = 10.0)
        :param put_circle_around_point:  (Default value = True)
        :param shrink:  (Default value = 0)
        :param marker: (Default value = None) A Marker

        """
        super().__init__(label_point.x, label_point.y)
        self.date = date
        self.text = text
        self.color = color
        self.bbox = bbox
        self.event_point = event_point
        self.font_size = font_size
        self.put_circle_around_point = put_circle_around_point
        self.shrink = shrink
        self.marker = marker
        self.relpos = relpos

    def set_bbox(self, bbox):
        """Set the bounding box of an annotation

        :param bbox: a matplotlib.transforms.Bbox instance

        """
        self.bbox = bbox
    
    def set_relpos(self, relpos):
        self.relpos = relpos

    def overlaps(self, that):
        """Check that the two Bboxes don't overlap
        
        They don't overlap if
            1) one rectangle's left side is strictly to the right other's right side
            2) one rectangle's top side is stricly bellow the other's bottom side

        :param that: an Annotation

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")

        if (self.bbox.xmin >= that.bbox.xmax or that.bbox.xmin >= self.bbox.xmax):
            return False

        # the coordinates are inverted, so y0 is larger than y1
        if (self.bbox.ymin >= that.bbox.ymax or that.bbox.ymin >= self.bbox.ymax):
            return False

        return True

    def is_within_epsilon_of(self, that, epsilon):
        """Check that the two are not at least as close as some epsilon
        
        :param that: An Annotation
        :param epsilon: A real number to define the tolerance for how close the label text can be

        """
        if (not isinstance(that, Annotation)):
            raise ValueError("Argument for intersects should be an annotation")

        if (self.bbox.xmin - epsilon > that.bbox.xmax or that.bbox.xmin - epsilon > self.bbox.xmax):
            return False

        if (self.bbox.ymin - epsilon > that.bbox.ymax or that.bbox.ymin - epsilon > self.bbox.ymax):
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
        width = min(self.bbox.xmax, that.bbox.xmax) - \
            max(self.bbox.xmin, that.bbox.xmin)
        height = min(self.bbox.ymax, that.bbox.ymax) - \
            max(self.bbox.ymin, that.bbox.ymin)

        return (width, height)

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
        """ """
        return f"Annotation '{self.text}' at {super().__repr__()}"

    def __str__(self):
        """ """
        return f"Annotation '{self.text}' at {super().__repr__()}"


class Era():
    """A class which shows a highlighted area on the graph to indicate a span of time"""

    def __init__(self, text, start, end, color, alpha=1):
        """

        :param text: The text to place on the graph
        :param start: A datetime.date indicating the start of the era
        :param end: A datetime.date indicating the end of the era
        :param color: A color useable by any matplotlib object

        """
        self.text = text
        self.start = start
        self.end = end
        self.color = color
        self.alpha = alpha

    def __repr__(self):
        """ """
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"

    def __str__(self):
        """ """
        return f"Era '{self.text}' starting at {self.start}, ending at {self.end}"


class EraSpan(Era):
    """A class which shows a dumbbell shape on the graph defining a span of your life"""

    def __init__(self, text, start, end, color, start_marker=None, end_marker=None):
        """

        :param text: The text to place on the graph
        :param start: A datetime.date indicating the start of the era
        :param end: A datetime.date indicating the end of the era
        :param color: A color useable by any matplotlib object
        :param start_marker: (Default = None) A marker for the starting point if one is wanted different than the default of the graph
        :param end_marker: (Default = None) A marker for the ending point if one is wanted different than the default of the graph

        """
        super().__init__(text, start, end, color)
        self.start_marker = start_marker
        self.end_marker = end_marker


class Papersize:
    """A class holding papersize in inches"""
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

    def __init__(self, birthdate, size=Papersize.A3, dpi=300, label_space_epsilon=0.2, max_age=90):
        """

        :param birthdate: 
        :param size:  (Default value = Papersize.A3)
        :param dpi:  (Default value = 300)
        :param label_space_epsilon:  (Default value = .2)
        :param show_watermark:  (Default value = False)

        """
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
        self.ymax = max_age

        self.xlims = [self.xmin, self.xmax]
        self.ylims = [self.ymin, self.ymax]

        self.fontsize = 25

        self.title = None
        self.title_fontsize = self.fontsize

        self.image_name = None
        self.image_alpha = 1

        self.xaxis_label = r'Week of the Year $\longrightarrow$'
        self.xaxis_color = 'b'
        self.xaxis_position = (0.20, 1.02)
        self.xaxis_fontsize = self.fontsize

        self.yaxis_label = r'$\longleftarrow$ Age'
        self.yaxis_color = 'b'
        self.yaxis_position = (-0.02, 0.95)
        self.yaxis_fontsize = self.fontsize

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

        self.watermark_text = None

        self.era_shrink = 10

        self.label_space_epsilon = label_space_epsilon

        self.annotations = []
        self.eras = []
        self.era_spans = []

    def format_x_axis(self, text=None, positionx=None, positiony=None, color=None, fontsize=None):
        if text is not None:
            self.xaxis_label = text

        x, y = self.xaxis_position
        if positionx is not None:
            x = positionx
        if positiony is not None:
            y = positiony
        self.xaxis_position = (x, y)

        if color is not None:
            self.xaxis_color = color

        if fontsize is not None:
            self.xaxis_fontsize = fontsize

    def format_y_axis(self, text=None, positionx=None, positiony=None, color=None, fontsize=None):
        if text is not None:
            self.yaxis_label = text

        x, y = self.yaxis_position
        if positionx is not None:
            x = positionx
        if positiony is not None:
            y = positiony
        self.yaxis_position = (x, y)

        if color is not None:
            self.yaxis_color = color

        if fontsize is not None:
            self.yaxis_fontsize = fontsize

    def show_max_age_label(self):
        """Places the max age on the bottom right of the plot"""
        self.ax.text(self.xmax+3, self.ymax, str(self.ymax),
                     fontsize=self.fontsize, color='black',
                     ha='center', va='bottom', transform=self.ax.transData)

    def add_life_event(self, text, date, color, hint=None, side=None, color_square=True):
        """ Label an event in your life

        :param text: param date: The date that the event occurred
        :param date: (Default value = None) When the event occurred
        :param color: (Default value = None) A color useable by any matplotlib object
        :param hint: (Default value = None) Mutually exclusive with side. Not required. If the default placement is not desired. A Point may be provided to help the graph decide where to place the label of the event.
        :param side: (Default value = None) Mutually exclusive with hint. Not required. If not provided, the side is determined by the date. If provided, this value will put the label on the given side of the plot
        :param color_square: (Default value = True) Colors the sqaure on the graph the same color as the text if True. The sqaure is the default color of the graph squares otherwise

        """
        logging.info(f"Adding life event '{text}' with color {color}")
        if (date < self.birthdate or date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

        week = int(np.floor((date - self.birthdate).days / 7)) + 1
        x = week % self.xmax
        y = int(np.floor(week / self.xmax))

        default_x = self.xmax if (x >= self.xmax / 2) else 0
        label_point = self.__get_label_point(hint, side, default_x, y)

        marker = None
        if color_square:
            marker = Marker(x, y, color=color)

        a = Annotation(date, text, label_point=label_point, color=color,
                       event_point=Point(x, y), shrink=self.annotation_marker_size / 2, marker=marker)
        self.annotations.append(a)

    def add_era(self, text, start_date, end_date, color, side=None, font_size=20, alpha=0.3):
        """

        :param text: The label text for the era
        :param start_date: When the event started
        :param end_date: When the event ended
        :param color: A color useable by any matplotlib object
        :param side: (Default value = None) Mutually exclusive with hint. Not required. If not provided, the side is determined by the date. If provided, this value will put the label on the given side of the plot
        :param font_size: (Default value = 20) the font size passed to matplotlib.axes.annotation

        """
        logging.info(f"Adding era '{text}' with color {color}")
        if (start_date < self.birthdate or start_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (end_date < self.birthdate or end_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)

        self.eras.append(Era(text, start_position, end_position, color, alpha=alpha))

        label_point = self.__get_label_point(
            hint=None, side=side, default_x=self.xmax, default_y=np.average((start_position.y, end_position.y)), is_Era=True)
        # when sorting the annotation the date is used
        # choose the middle date so that the annotation ends up
        # as close to the middle of the era as possible
        # if no hint was provided
        middle_date = start_date + (end_date - start_date)/2

        a = Annotation(middle_date, text, label_point=label_point, color=color,
                       event_point=label_point, font_size=font_size, put_circle_around_point=False, shrink=self.era_shrink)
        self.annotations.append(a)

    def add_era_span(self, text, start_date, end_date, color='g', hint=None, side=None, color_start_and_end_markers=False):
        """

        :param text: param start_date:
        :param start_date:
        :param end_date:
        :param color: Default value = 'g')
        :param hint: Default value = None)
        :param side: Default value = None)
        :param color_start_and_end_markers: (Default value = False) Colors the sqaures indicating the start and end date on the graph the same color as the text if True. The sqaures are the default color of the graph squares otherwise

        """
        logging.info(f"Adding era span '{text}' with color {color}")
        if (start_date < self.birthdate or start_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")
        if (end_date < self.birthdate or end_date > (relativedelta(years=self.ymax) + self.birthdate)):
            raise ValueError(
                f"The event date must be a valid datetime.date object that is at least as recent as the birthdate and no larger than {self.ymax}")

        start_position = self.__to_date_position(start_date)
        end_position = self.__to_date_position(end_date)
        label_point = self.__get_label_point(
            hint, side, self.xmax, np.average((start_position.y, end_position.y)))

        start_marker = None
        end_marker = None
        if color_start_and_end_markers:
            start_marker = Marker(
                start_position.x, start_position.y, color=color)
            end_marker = Marker(end_position.x, end_position.y, color=color)

        # this will put a dumbbell onto the graph spanning the era
        self.era_spans.append(EraSpan(text, start_position, end_position,
                                      color, start_marker=start_marker, end_marker=end_marker))

        middle_date = start_date + (end_date - start_date)/2

        event_point = Point(np.average((start_position.x, end_position.x)), np.average(
            (start_position.y, end_position.y)))

        self.annotations.append(Annotation(middle_date, text, label_point=label_point,
                                           color=color, event_point=event_point, font_size=20.0, put_circle_around_point=False))

    def add_watermark(self, text):
        """

        :param text: 

        """
        self.watermark_text = text

    def add_title(self, text, fontsize=None):
        self.title = text
        if fontsize is not None:
            self.title_fontsize = fontsize

    def add_image(self, image_name, alpha=1):
        self.image_name = image_name
        self.image_alpha = alpha

    def show(self):
        """ """
        self.ax.show()

    def close(self):
        """ """
        self.ax.close()

    def save(self, name, transparent=False):
        """

        :param name: param transparent:  (Default value = False)
        :param transparent: Default value = False)

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

        self.__draw_xaxis()
        self.__draw_yaxis()

        self.__draw_annotations()
        self.__draw_eras()
        self.__draw_era_spans()
        self.__draw_watermark()
        self.__draw_title()
        self.__draw_image()

        # hide the horizontal and vertical lines
        self.ax.set_frame_on(False)

        self.ax.set_aspect('equal', adjustable='box', share=True)

    def __draw_xaxis(self):
        """ """
        self.ax.set_xlim(self.xlims)
        # put x ticks on top
        xticks = [1]
        xticks.extend(range(5, self.xmax+5, 5))
        self.ax.xaxis.tick_top()
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(xticks[:-1])
        self.ax.set_xlabel(self.xaxis_label,
                           color=self.xaxis_color, fontsize=self.xaxis_fontsize)
        self.ax.xaxis.set_label_position('top')
        self.ax.xaxis.set_label_coords(*self.xaxis_position)
        self.ax.xaxis.set_tick_params(
            width=0, direction='out', pad=self.inner_padx)

    def __draw_yaxis(self):
        """ """
        self.ax.set_ylim(self.ylims)
        # set y ticks
        yticks = [*range(0, self.ymax, 5)]
        self.ax.set_yticks(yticks)
        self.ax.set_ylabel(self.yaxis_label,
                           color=self.yaxis_color, fontsize=self.yaxis_fontsize)
        self.ax.yaxis.set_label_coords(*self.yaxis_position)
        self.ax.yaxis.set_tick_params(
            width=0, direction='in', pad=self.inner_pady)
        self.ax.invert_yaxis()

    def __draw_annotations(self):
        """ """
        final = self.__resolve_annotation_conflicts(self.annotations)

        for a in final:
            if a.put_circle_around_point:
                self.ax.plot(a.event_point.x, a.event_point.y, marker='o', color=a.color,
                             markerfacecolor='none', ms=self.annotation_marker_size, mew=self.annotation_edge_width)

            if a.marker is not None:
                self.ax.plot(a.marker.x, a.marker.y, color=a.marker.color, marker=a.marker.marker,
                             fillstyle=a.marker.fillstyle, linestyle='none', mew=self.grid_mew)

            self.ax.annotate(a.text, xy=(a.event_point.x, a.event_point.y), xytext=(a.x, a.y),
                             weight='bold', color=a.color, size=a.font_size, va='center',
                             arrowprops=dict(arrowstyle='-',
                                             connectionstyle="arc3",
                                             color=a.color,
                                             shrinkB=a.shrink,
                                             relpos=a.relpos)) #search for 'relpos' on https://matplotlib.org/tutorials/text/annotations.html

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
                                    alpha=era.alpha, xmin=axesUnits[0], xmax=xmax)
                elif y == era.end.y:
                    axesUnits = self.ax.transLimits.transform(
                        (era.end.x+.5, era.end.y))
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=era.alpha, xmin=xmin, xmax=axesUnits[0])
                else:
                    self.ax.axhspan(y-.5, y+.5, facecolor=era.color,
                                    alpha=era.alpha, xmin=xmin, xmax=xmax)

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

            if era.start_marker is not None:
                self.ax.plot(era.start_marker.x, era.start_marker.y, color=era.start_marker.color, marker=era.start_marker.marker,
                             fillstyle=era.start_marker.fillstyle, linestyle='none', mew=self.grid_mew)

            if era.end_marker is not None:
                self.ax.plot(era.end_marker.x, era.end_marker.y, color=era.end_marker.color, marker=era.end_marker.marker,
                             fillstyle=era.end_marker.fillstyle, linestyle='none', mew=self.grid_mew)

            l = mlines.Line2D([x1, x2], [y1, y2], color=era.color)
            self.ax.add_line(l)

    def __draw_watermark(self):
        """ """
        if self.watermark_text is not None:
            self.fig.text(0.5, 0.5, self.watermark_text,
                          fontsize=100, color='gray',
                          ha='center', va='center', alpha=0.3, rotation=65, transform=self.ax.transAxes)

    def __draw_title(self):
        if self.title is not None:
            self.fig.suptitle(self.title, fontsize=self.title_fontsize)

    def __draw_image(self):
        if self.image_name is not None:
            img = mpimg.imread(self.image_name)
            extent = (0.5, self.xmax+0.5, -0.5, self.ymax-0.5)
            self.ax.imshow(img, extent=extent, origin='lower', alpha=self.image_alpha)

    def __resolve_annotation_conflicts(self, annotations):
        """Put annotation text labels on the graph while avoiding conflicts.

        This method decides the final (x, y) coordinates for the graph such that
        no two text label bounding boxes overlap. This happens by placing the labels
        from the top of the graph to the bottom. If any label were to overlap with
        another, it is moved down graph by the amount that it overlaps plus a buffer
        amount of space. The annotations are also sorted by their event date, so
        that labels pointing to the same line will avoid having their arcs overlap
        each other.

        :param annotations: param side:

        """
        # set the bounding box and initial positions of the annotations
        # the x-value is only corrected if it is inside the graph or too close to the graph
        left = []
        right = []
        for a in annotations:
            # first, get the bounds
            self.__set_annotation_bbox(a)

            # now set the intitial positions
            # we want all of the text to be on the left or right of the squares
            width = a.bbox.width
            # to preserve hint values, only set the x value if it is inside the graph
            # or if it is not at least as far as the offset
            if ((a.x >= self.xmax / 2) and (a.x < self.xmax)) or (a.x >= self.xmax and a.x < self.xmax + self.right_annotation_offset):
                a.x = self.xmax + self.right_annotation_offset
            elif ((a.x >= 0) and (a.x < self.xmax / 2)) or (a.x <= self.xmin and a.x > self.xmin - self.left_annotation_offset):
                a.x = self.xmin - self.left_annotation_offset - width
            a.bbox.x0 = a.x
            a.bbox.x1 = a.x + width
            if (a.x >= self.xmax / 2):
                a.set_relpos((0, 0.5))
                right.append(a)
            if (a.x < self.xmax / 2):
                a.set_relpos((1, 0.5))
                left.append(a)

        left.sort(key=lambda a: a.date)
        right.sort(key=lambda a: (a.event_point.y, -a.event_point.x))

        final = []
        for lst in [left, right]:
            _f = []
            for unchecked in lst:
                for checked in _f:
                    if unchecked.overlaps(checked):
                        correction = unchecked.xy_overlapping_width_height(
                            checked, self.label_space_epsilon)
                        unchecked.update_Y_with_correction(correction)
                    if unchecked.is_within_epsilon_of(checked, self.label_space_epsilon):
                        correction = [0, self.label_space_epsilon]
                        unchecked.update_Y_with_correction(correction)
                _f.append(unchecked)
            final.extend(_f)

        return final

    def __to_date_position(self, date):
        """

        :param date: 

        """
        week = int(np.floor((date - self.birthdate).days / 7)) + 1
        x = week % self.xmax
        y = int(np.floor(week / self.xmax))
        year_of_life = y
        return DatePosition(x, y, week, year_of_life, date)

    def __sanitize_hint(self, hint):
        """Hints should have an x value < 0 or bigger than self.xmax

        :param hint: 

        """
        # TODO: what should this be?
        edge = 10
        if hint is not None:
            if (hint.x >= self.xmax / 2 and hint.x < self.xmax) or hint.x > self.xmax + edge:
                hint.x = self.xmax
            if (hint.x > 0 and hint.x < self.xmax / 2) or hint.x < -edge:
                hint.x = 0

        return hint

    def __set_annotation_bbox(self, a):
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
        a.set_bbox(Bbox(bbox_data_units))
        t.remove()

    def __get_label_point(self, hint=None, side=None, default_x=0, default_y=0, is_Era=False):
        """

        :param hint: 
        :param side: 
        :param start_position: 
        :param end_position: 

        """
        if (hint is not None and side is not None):
            raise ValueError(
                f"Hint and side are mutually exclusive arguments. Specify only one of them.")
        hint = self.__sanitize_hint(hint)
        labelx = default_x
        labely = default_y

        if hint is not None:
            labelx = hint.x
            labely = hint.y

        if side is not None:
            if side == Side.LEFT:
                labelx = 0 if is_Era == False else 1
            else:
                labelx = self.xmax

        return Point(labelx, labely)
