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

    def __init__(self, row, col, initial_state):
        self.x = row
        self.y = col
        self.is_white_face = initial_state == "0"
        self.__assign_identifier()

    def __assign_identifier(self):
        self.identifier = "{}{}".format(alphabet[self.x], self.y)

    def flip(self):
        self.is_white_face = not self.is_white_face

    def __str__(self):
        return "0" if self.is_white_face else "1"


class Board:
    """
    Indonesian Dot Puzzle board holding 2d of token
    """

    def __init__(self, initial_state_stream, size):
        self.content = [[Token(row, col, initial_state_stream[col + row * size])
                         for col in range(size)] for row in range(size)]

    def __str__(self):
        return ' '.join([x_token.__str__() for y_token in self.content for x_token in y_token])


class Solver:
    """
    Context for SearchStrategy/Solver for the puzzle
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def solve(self, initial_board: Board):
        self.strategy.execute(initial_board)


class Game:
    """
    Model to hold games described by a single line in the input file
    """

    def __init__(self, size, max_depth, max_length, board_stream):
        self.size = size
        if MIN_BOARD_SIZE > size > MAX_BOARD_SIZE:
            print("Given size is out of bounds, defaulting to minimum size...")
            self.size = MIN_BOARD_SIZE
        else:
            self.size = size

        self.max_depth = max_depth
        self.max_length = max_length
        self.board_stream = board_stream

    def get_game_board(self):
        return Board(self.board_stream, self.size)

    def get_max_depth(self):
        return self.max_depth

    def get_max_length(self):
        return self.max_length
