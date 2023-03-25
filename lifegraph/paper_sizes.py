from enum import Enum

class Papersize(Enum):
    """A class holding papersize in inches"""
    A0 = 1,
    A1 = 2,
    A2 = 3,
    A3 = 4,
    A4 = 5,
    A5 = 6,
    A6 = 7,
    A7 = 8,
    A8 = 9,
    A9 = 10,
    A10 = 11,
    HalfLetter = 12,
    Letter = 13,
    Legal = 14,
    JuniorLegal = 15,
    Ledger = 16,
    Tabloid = 17

    # all sizes are in inches
    sizes = {
        A0 : [33.1, 46.8],
        'A0' : [33.1, 46.8],
        A1 : [23.4, 33.1],
        'A1' : [23.4, 33.1],
        A2 : [16.5, 23.4],
        'A2' : [16.5, 23.4],
        A3 : [11.7, 16.5],
        'A3' : [11.7, 16.5],
        A4 : [8.3, 11.7],
        'A4' : [8.3, 11.7],
        A5 : [5.8, 8.3],
        'A5' : [5.8, 8.3],
        A6 : [4.1, 5.8],
        'A6' : [4.1, 5.8],
        A7 : [2.9, 4.1],
        'A7' : [2.9, 4.1],
        A8 : [2.0, 2.9],
        'A8' : [2.0, 2.9],
        A9 : [1.5, 2.0],
        'A9' : [1.5, 2.0],
        A10 : [1.0, 1.5],
        'A10' : [1.0, 1.5],
        HalfLetter : [5.5, 8.5],
        'HalfLetter' : [5.5, 8.5],
        Letter : [8.5, 11.0],
        'Letter' : [8.5, 11.0],
        Legal : [8.5, 14.0],
        'Legal' : [8.5, 14.0],
        JuniorLegal : [5.0, 8.0],
        'JuniorLegal' : [5.0, 8.0],
        Ledger : [11.0, 17.0],
        'Ledger' : [11.0, 17.0],
        Tabloid : [17.0, 11.0],
        'Tabloid' : [17.0, 11.0],
    }

    def to_matplotlib_size(self, size):
        """ Given a Papersize, return a tuple of that paper size, in inches

        :param size: A Papersize enum or string
        """

        return self.sizes[size]