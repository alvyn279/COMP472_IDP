from abc import ABC, abstractmethod
from models.game import Board
from typing import List


class SearchStrategy(ABC):
    """
    Strategy interface for the different algorithms that will be used
    to solve Indonesian Dot Puzzle
    """

    @abstractmethod
    def execute(self, initial_board: Board):
        pass


class DepthFirstSearchStrategy(SearchStrategy):
    """
    Depth-first search strategy
    Follows the concept of depth-limited search
    """

    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.closed_list_set = set()
        self.open_list = []  # type: List[Board]
        self.open_list_set = set()
        self.current_depth = 0

    def execute(self, board: Board):
        self.open_list.append(board)

        while len(self.open_list) != 0:
            self.current_depth = 1

            while self.current_depth <= self.max_depth:
                board_to_test = self.open_list.pop()

                if board_to_test.is_final_state():
                    print("\nFound solution!\n")
                    return
                else:
                    self.closed_list_set.add(board_to_test)

                for x_token in range(board.size):
                    for y_token in range(board.size):
                        new_board = Board(board_to_test.get_state_stream(), board.size)
                        token_to_test = new_board.content[x_token][y_token]

                        x = token_to_test.x
                        y = token_to_test.y

                        # change state after touch
                        new_board.content[x][y].is_white_face = not new_board.content[x][y].is_white_face
                        if x > 0:
                            new_board.content[x - 1][y].is_white_face = not new_board.content[x - 1][y].is_white_face
                        if x < len(new_board.content - 1):
                            new_board.content[x + 1][y].is_white_face = not new_board.content[x + 1][y].is_white_face
                        if y > 0:
                            new_board.content[x][y - 1].is_white_face = not new_board.content[x][y - 1].is_white_face
                        if y < len(new_board.content[x] - 1):
                            new_board.content[x][y + 1].is_white_face = not new_board.content[x][y + 1].is_white_face

                        if new_board.get_state_stream() not in self.closed_list_set:
                            self.open_list.append(new_board)

                self.current_depth += 1
