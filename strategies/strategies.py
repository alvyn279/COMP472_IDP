from abc import ABC, abstractmethod
from models.game import Board, MoveSnapshot, Game
from typing import List, Tuple
from constants.constants import \
    NO_SOLUTION, \
    FOUND_SOLUTION, \
    DFS, \
    REL_PATH_TO_SEARCH, \
    REL_PATH_TO_SOLUTION, \
    BFS
import os


class SearchStrategy(ABC):
    """
    Strategy interface for the different algorithms that will be used
    to solve Indonesian Dot Puzzle
    """

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _generate_output(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, initial_board: Board):
        pass


class DepthFirstSearchStrategy(SearchStrategy):
    """
    Depth-first search strategy
    Follows the concept of depth-limited search
    """

    name = DFS

    def __init__(self, game: Game):
        self.game = game
        self.current_depth = 0
        self.max_depth = game.max_depth
        self.open_list = []  # type: List[Tuple[Board, MoveSnapshot]]
        self.closed_list_set = set()
        self.result_move_snapshots = []  # type: List[MoveSnapshot]
        self.shortest_move_snapshots = []  # type: List[MoveSnapshot]
        self.search_seq_snapshots = []  # type: List[MoveSnapshot]

    def _generate_output(self):
        """
        Generates the solution and search files for DFS
        Particularity: finds the shortest path, as per the problem statement
        """
        cur_dir = os.path.dirname(__file__)
        # solution file
        abs_sol_path = os.path.join(cur_dir, REL_PATH_TO_SOLUTION.format(self.game.game_id, self.name))
        sol_f = open(abs_sol_path, "w+")
        if len(self.shortest_move_snapshots) == 0:
            sol_f.write(NO_SOLUTION)
        else:
            for shortest_move_snapshot in self.shortest_move_snapshots:
                sol_f.write(shortest_move_snapshot.__str__() + '\n')
        sol_f.close()

        # search file
        abs_srch_path = os.path.join(cur_dir, REL_PATH_TO_SEARCH.format(self.game.game_id, self.name))
        srch_f = open(abs_srch_path, "w+")
        for search_seq_snapshot in self.search_seq_snapshots:
            srch_f.write("0\t0\t0\t{}\n".format(search_seq_snapshot.board_snapshot.replace(' ', '')))
        srch_f.close()

    def __alert_end(self):
        """
        Prints to console the shortest path for DFS and/or status of the search
        """
        if len(self.shortest_move_snapshots) != 0:
            print("\n{}\n".format(FOUND_SOLUTION))
            for shortest_move_snapshot in self.shortest_move_snapshots:
                print(shortest_move_snapshot)

            print(len(self.shortest_move_snapshots))
        else:
            print("\n{}".format(NO_SOLUTION))
        self._generate_output()

    def execute(self, board: Board):
        self.current_depth = 1
        self.open_list.append((board, MoveSnapshot('0 ', board.__str__(), self.current_depth)))

        while len(self.open_list) != 0:
            board_to_test, snapshot = self.open_list.pop()
            self.search_seq_snapshots.append(snapshot)

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
                              key=lambda _board_snapshot_tuple: _board_snapshot_tuple[0],
                              reverse=True)
            # print(children)
            self.open_list += children

        self.__alert_end()


class HeuristicSearchStrategy(SearchStrategy):
    """
    Strategy model that holds the heuristic function used for heuristic-based search
    """

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _generate_output(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, initial_board: Board):
        pass

    def _is_even(self, number: int) -> bool:
        return number % 2 == 0

    def _build_expected_even_stream(self, n: int, start_char: str):
        """
        Builds the expected stream of characters expected for the even case of checkered-state
        :param n:
        :param start_char:
        :return:
        """
        row_switcher = '1' if start_char == '1' else '0'
        expected_stream = []

        for x in range(n):
            switcher = '1' if row_switcher == '1' else '0'
            for y in range(n):
                expected_stream.append(switcher)
                switcher = '0' if switcher == '1' else '1'
            row_switcher = '0' if row_switcher == '1' else '1'

        return expected_stream

    def checkered_heuristic(self, board: Board) -> int:
        """
        Looks for the number of inconsistencies from an expected state where all the tokens are
        positioned in a checkered position relative to one another.
        :param board:
        :return:
        """
        board_state_stream = board.get_state_stream()
        inconsistencies = 0

        if self._is_even(board.size):
            expected_stream = self._build_expected_even_stream(board.size, board_state_stream[0])
            actual_stream = list(board_state_stream)

            if len(expected_stream) != len(actual_stream):
                raise Exception('Board state length does not match expected state length')

            inconsistencies = sum(1 for i, j in zip(expected_stream, actual_stream) if i != j)

        else:
            # TODO: could be generator
            switcher = '1' if board_state_stream.startswith(1) else '0'

            for char in board_state_stream:
                if char != switcher:
                    inconsistencies += 1
                switcher = '0' if switcher == '1' else '1'

        return inconsistencies


class BestFirstSearchStrategy(HeuristicSearchStrategy):
    """
    Best-first search strategy
    Follows the concept of a heuristic search, while choosing the smallest
    return value for a heuristic function from the open list
    """

    name = BFS

    def __init__(self, game: Game):
        self.game = game
        self.current_path_length = 0
        self.max_search_path_length = game.max_length
        self.open_list = []  # type: List[Tuple[Board, MoveSnapshot]]
        self.closed_list_set = set()
        self.result_move_snapshots = []  # type: List[MoveSnapshot]
        self.shortest_move_snapshots = []  # type: List[MoveSnapshot]
        self.search_seq_snapshots = []  # type: List[MoveSnapshot]

    def _generate_output(self):
        raise NotImplementedError

    def execute(self):
        pass
