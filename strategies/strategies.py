from abc import ABC, abstractmethod
from models.game import Board, MoveSnapshot
from typing import List, Tuple


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
        self.current_depth = 0
        self.max_depth = max_depth
        self.open_list = []  # type: List[Tuple[Board, MoveSnapshot]]
        self.closed_list_set = set()
        self.result_move_snapshots = []  # type: List[MoveSnapshot]
        self.shortest_move_snapshots = []  # type: List[MoveSnapshot]

    @staticmethod
    def __board_snapshot_tuple_sorter(item):
        return item[0]

    def __alert_end(self):
        if len(self.shortest_move_snapshots) != 0:
            print("\nFound solution!\n")
            for shortest_move_snapshot in self.shortest_move_snapshots:
                print(shortest_move_snapshot)

            print(len(self.shortest_move_snapshots))
        else:
            print("\nNo solution found")

    def execute(self, board: Board):
        self.current_depth = 1
        self.open_list.append((board, MoveSnapshot('0 ', board.__str__(), self.current_depth)))

        while len(self.open_list) != 0:
            board_to_test, snapshot = self.open_list.pop()

            if board_to_test.is_final_state():
                self.result_move_snapshots.append(snapshot)

                # keep state of shortest path
                if len(self.result_move_snapshots) < len(self.shortest_move_snapshots) \
                        or len(self.shortest_move_snapshots) == 0:
                    self.shortest_move_snapshots = self.result_move_snapshots.copy()
                self.result_move_snapshots.pop()
            else:
                self.closed_list_set.add(board_to_test.get_state_stream())

            # analyze board state from open list
            if self.current_depth + 1 > self.max_depth:
                self.current_depth = snapshot.depth
                self.result_move_snapshots = self.result_move_snapshots[0:snapshot.depth - 1]
                continue
            else:
                self.result_move_snapshots.append(snapshot)
                self.current_depth += 1

            children: List[Tuple[Board, MoveSnapshot]] = []

            # uncover children
            for x_token in range(board.size):
                for y_token in range(board.size):

                    new_board = Board(board_to_test.get_state_stream(), board.size)
                    token_to_test = new_board.content[x_token][y_token]

                    x = token_to_test.x
                    y = token_to_test.y

                    # change state after touch
                    new_board.content[x][y].flip()
                    if x > 0:
                        new_board.content[x - 1][y].flip()
                    if x < (len(new_board.content) - 1):
                        new_board.content[x + 1][y].flip()
                    if y > 0:
                        new_board.content[x][y - 1].flip()
                    if y < (len(new_board.content[x]) - 1):
                        new_board.content[x][y + 1].flip()

                    if new_board.get_state_stream() not in self.closed_list_set:
                        children.insert(0, (
                            new_board,
                            MoveSnapshot(token_to_test.get_identifier(), new_board.__str__(), self.current_depth)
                        ))

            # sort children according to first occurrence of a white
            children = sorted(children,
                              key=self.__board_snapshot_tuple_sorter,
                              reverse=True)
            # print(children)
            self.open_list += children

        self.__alert_end()
