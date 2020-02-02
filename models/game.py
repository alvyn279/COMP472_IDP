from constants.constants import MAX_BOARD_SIZE, MIN_BOARD_SIZE
from string import ascii_uppercase

alphabet = list(ascii_uppercase)


class Token:
    """
    Wooden token used to place on board
    2 states:
        - white face
        - black face
    """

    def __init__(self, x, y):
        self.isWhiteFace = True
        self.x = x
        self.y = y
        self.__assign_identifier()

    def __assign_identifier(self):
        self.identifier = "{}{}".format(alphabet[self.x], self.y)

    def flip(self):
        self.isWhiteFace = not self.isWhiteFace


class Board:
    """
    Indonesian Dot Puzzle board
    """

    def __init__(self, size=0):

        if MIN_BOARD_SIZE > size > MAX_BOARD_SIZE:
            print("Given size is out of bounds, defaulting to minimum size...")
            self.size = MIN_BOARD_SIZE
        else:
            self.size = size

        self.board = [[Token(i, j) for i in range(size)] for j in range(size)]
