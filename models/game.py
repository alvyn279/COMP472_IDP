from constants.constants import MAX_BOARD_SIZE, MIN_BOARD_SIZE
from strategies.strategies import SearchStrategy
from string import ascii_uppercase

alphabet = list(ascii_uppercase)


class Token:
    """
    Wooden token used to place on board
    2 states:
        - white face
        - black face
    """

    def __init__(self, row, col, initial_state):
        self.x = row
        self.y = col
        self.is_white_face = initial_state == 0
        self.__assign_identifier()

    def __assign_identifier(self):
        self.identifier = "{}{}".format(alphabet[self.x], self.y)

    def flip(self):
        self.is_white_face = not self.is_white_face


class Board:
    """
    Indonesian Dot Puzzle board holding 2d of token
    """

    def __init__(self, initial_state_stream="000000000", size=MIN_BOARD_SIZE):

        if MIN_BOARD_SIZE > size > MAX_BOARD_SIZE:
            print("Given size is out of bounds, defaulting to minimum size...")
            self.size = MIN_BOARD_SIZE
        else:
            self.size = size

        self.content = [[Token(row, col, initial_state_stream[col + row * self.size])
                         for col in range(self.size)] for row in range(self.size)]


class Solver:
    """
    Context for SearchsStrategy/Solver for the puzzle
    """

    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def solve(self, initial_board: Board):
        self.strategy.execute(initial_board)
