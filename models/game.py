from constants.constants import MAX_BOARD_SIZE, MIN_BOARD_SIZE
from string import ascii_uppercase
from typing import List
import time

alphabet = list(ascii_uppercase)


class Token:
    """
    Wooden token used to place on board
    2 states:
        - white face
        - black face
    """

    def __init__(self, row: int, col: int, initial_state: str):
        self.x = row
        self.y = col
        self.is_white_face = initial_state == "0"
        self.__assign_identifier()

    def __assign_identifier(self):
        self._identifier = "{}{}".format(alphabet[self.x], self.y)

    def flip(self):
        self.is_white_face = not self.is_white_face

    def get_identifier(self):
        return self._identifier

    def __str__(self):
        return "0" if self.is_white_face else "1"


class Board:
    """
    Indonesian Dot Puzzle board holding 2d of token
    """

    def __init__(self, initial_state_stream: str, size: int):
        self.size = size
        self.content = [[Token(row, col, initial_state_stream[col + row * size])
                         for col in range(size)] for row in range(size)]
        self.remaining_black_dots = self.__init_remaining_black_dots()

    def __init_remaining_black_dots(self):
        agg = []  # type: List[Token]

        for row in range(self.size):
            for col in range(self.size):
                if not self.content[row][col].is_white_face:
                    agg.append(self.content[row][col])

        return agg

    def __stream_iterator(self, joiner: str):
        return joiner.join([x_token.__str__() for y_token in self.content for x_token in y_token])

    def get_state_stream(self):
        return self.__stream_iterator('')

    def is_final_state(self):
        return len(self.__init_remaining_black_dots()) == 0

    def __str__(self):  # hash
        return self.__stream_iterator(' ')

    def __repr__(self):
        return self.__stream_iterator(' ')

    def __lt__(self, other):
        return self.get_state_stream() < other.get_state_stream()


class MoveSnapshot:
    """
    Model that will keep track of a token that was touched, as well as the resulting
    board state that resulted from the touch
    """

    def __init__(self, token_id: str, board: str, depth: int = 0):
        self.token = token_id
        self.board_snapshot = board
        # store the depth at which the board snapshot was taken, to make sure to restore
        # the correct state of the answer path while backtracking
        self.depth = depth

    def __str__(self):
        return '{}\t{}'.format(self.token, self.board_snapshot)


class OpenListSnapshot:
    """
    Model that holds MoveSnapshot and Board states but also a priority representation
    """

    def __init__(self, board: Board, move_snapshot: MoveSnapshot, priority: int):
        self.board = board
        self.move_snapshot = move_snapshot
        self.priority = priority

    def get_board(self):
        return self.board

    def get_move_snapshot(self):
        return self.move_snapshot

    def __lt__(self, other):
        return self.priority < other.priority


class Game:
    """
    Model to hold games described by a single line in the input file
    """

    def __init__(self, size: int, max_depth: int, max_length: int, board_stream: str, game_id: int):
        self.game_id = game_id
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


class Solver:
    """
    Context for SearchStrategy/Solver for the puzzle
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def solve(self, initial_board: Board):
        start = time.time()
        self.strategy.execute(initial_board)
        end = time.time()
        print("\nTime for {} : {} seconds".format(type(self.strategy).__name__, end - start))
