from abc import ABC, abstractmethod
from exceptions.exceptions import ExceedingSearchPathLengthError
from models.game import Board, MoveSnapshot, Game, OpenListSnapshot, Token
from typing import List, Tuple, Set
from constants.constants import \
    NO_SOLUTION, \
    FOUND_SOLUTION, \
    DFS, \
    REL_PATH_TO_SEARCH, \
    REL_PATH_TO_SOLUTION, \
    BeFS, \
    ASTAR
import os

import queue as Q


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

    def __init__(self, game: Game):
        self.game = game
        self.current_depth = -1
        self.open_list = Q.PriorityQueue()  # type: Q.PriorityQueue[OpenListSnapshot]
        self.open_list_set = set()  # type: Set[str]
        self.closed_list_set = set()  # type: Set[str]
        self.result_move_snapshots = []  # type: List[MoveSnapshot]
        self.search_path_snapshots = []  # type: List[MoveSnapshot]

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def _add_to_priority_queue(self, new_board: Board, token_to_test: Token) -> List[OpenListSnapshot]:
        """
        Defines the parameters of the priority with which the move is added to the priority queue
        :param new_board:
        :param token_to_test:
        :return:
        """
        pass

    def _generate_output(self, no_solution=False):
        """
        Generates the solution and search files
        """

        cur_dir = os.path.dirname(__file__)
        # solution file
        abs_sol_path = os.path.join(cur_dir, REL_PATH_TO_SOLUTION.format(self.game.game_id, self.name))
        sol_f = open(abs_sol_path, "w+")
        if no_solution:
            sol_f.write(NO_SOLUTION)
        else:
            for result_move_snapshot in self.result_move_snapshots:
                sol_f.write(result_move_snapshot.__str__() + '\n')
        sol_f.close()

        # search file
        abs_srch_path = os.path.join(cur_dir, REL_PATH_TO_SEARCH.format(self.game.game_id, self.name))
        srch_f = open(abs_srch_path, "w+")
        for search_path_snapshot in self.search_path_snapshots:
            srch_f.write('{}\t{}\t{}\t{}\n'
                         .format(search_path_snapshot.f_of_n,
                                 search_path_snapshot.g_of_n,
                                 search_path_snapshot.h_of_n,
                                 search_path_snapshot.__str__())
                         )
        srch_f.close()

    def _alert_end(self, no_solution=False):
        """
        Prints to console the resulting sequence
        :param no_solution:
        :return:
        """

        if not no_solution:
            print("\n{}\n".format(FOUND_SOLUTION))
            for result_move_snapshot in self.result_move_snapshots:
                print(result_move_snapshot)

        else:
            print("\n{}".format(NO_SOLUTION))

        self._generate_output(no_solution)
        pass

    def _is_even(self, number: int) -> bool:
        """
        Helper to determine if a number is even
        :param number:
        :return:
        """
        return number % 2 == 0

    def _build_expected_even_stream(self, n: int, start_char: str) -> List[str]:
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
        Assumed to be admissible, see report for example
        :param board:
        :return:
        """
        board_state_stream: str = board.get_state_stream()
        inconsistencies = 0

        # if board is perfect set to max priority
        if board.is_final_state():
            return 0

        if self._is_even(board.size):
            expected_stream = self._build_expected_even_stream(board.size, board_state_stream[0])
            actual_stream = list(board_state_stream)

            if len(expected_stream) != len(actual_stream):
                raise Exception('Board state length does not match expected state length')

            inconsistencies = sum(1 for i, j in zip(expected_stream, actual_stream) if i != j)

        else:
            # TODO: could be generator
            switcher = '1' if board_state_stream.startswith('1') else '0'

            for char in board_state_stream:
                if char != switcher:
                    inconsistencies += 1
                switcher = '0' if switcher == '1' else '1'

        return inconsistencies

    def execute(self, board: Board):
        self.open_list.put(OpenListSnapshot(board, MoveSnapshot('0 ', board.__str__()), 0))

        try:
            while not self.open_list.empty():
                open_list_snapshot = self.open_list.get()  # poll from priority queue
                board_to_test = open_list_snapshot.get_board()
                snapshot = open_list_snapshot.get_move_snapshot()
                self.search_path_snapshots.append(snapshot)

                # handle an element polled from priority queue that does not follow current solution path
                if snapshot.depth != self.current_depth:
                    self.current_depth = snapshot.depth
                    self.result_move_snapshots = self.result_move_snapshots[0:snapshot.depth]

                # check for end conditions
                if board_to_test.is_final_state():
                    self.result_move_snapshots.append(snapshot)
                    break
                elif len(self.search_path_snapshots) > self.game.max_length:
                    raise ExceedingSearchPathLengthError("Assuming no solution for BFS")
                self.current_depth += 1

                # add board to test to potential solution and uncover its children
                self.result_move_snapshots.append(snapshot)
                self.closed_list_set.add(board_to_test.get_state_stream())
                children: List[OpenListSnapshot] = []

                for x_token in range(board.size):
                    for y_token in range(board.size):

                        new_board = Board(board_to_test.get_state_stream(), board.size)
                        token_to_test = new_board.content[x_token][y_token]

                        x = token_to_test.x
                        y = token_to_test.y

                        new_board.content[x][y].flip()
                        if x > 0:
                            new_board.content[x - 1][y].flip()
                        if x < (len(new_board.content) - 1):
                            new_board.content[x + 1][y].flip()
                        if y > 0:
                            new_board.content[x][y - 1].flip()
                        if y < (len(new_board.content[x]) - 1):
                            new_board.content[x][y + 1].flip()

                        # create list of OpenListSnapshot objects with custom priority
                        children += self._add_to_priority_queue(new_board, token_to_test)

                for child in children:
                    # offer to priority queue
                    self.open_list.put(child)
                    self.open_list_set.add(child.get_board().get_state_stream())

            self._alert_end(False)

        except ExceedingSearchPathLengthError:
            self._alert_end(True)


class BestFirstSearchStrategy(HeuristicSearchStrategy):
    """
    Best-first search strategy
    Follows the concept of a heuristic search, while choosing the smallest
    return value for a heuristic function from the open list
    """

    name = BeFS

    def __init__(self, game: Game):
        HeuristicSearchStrategy.__init__(self, game)

    def _add_to_priority_queue(self, new_board: Board, token_to_test: Token) -> List[OpenListSnapshot]:
        """
        Adds to priority queue solely with knowledge of heuristic function h(n)
        :param new_board:
        :param token_to_test:
        :return:
        """
        children: List[OpenListSnapshot] = []

        if new_board.get_state_stream() not in self.closed_list_set \
                and new_board.get_state_stream() not in self.open_list_set:
            estimate_current_to_finish = self.checkered_heuristic(new_board)  # h(n)
            priority_val: int = estimate_current_to_finish
            new_move_snapshot: MoveSnapshot = MoveSnapshot(token_to_test.get_identifier(),
                                                           new_board.__str__(),
                                                           self.current_depth + 1)
            new_move_snapshot.set_eval(0, estimate_current_to_finish)
            children.append(OpenListSnapshot(
                new_board,
                new_move_snapshot,
                priority_val
            ))

        return children


class AStarSearchStrategy(HeuristicSearchStrategy):
    """
    A* search strategy, assumes heuristic function is admissible,
    where h(n) <= h*(n)
    """

    name = ASTAR

    def __init__(self, game: Game):
        HeuristicSearchStrategy.__init__(self, game)

    def _add_to_priority_queue(self, new_board: Board, token_to_test: Token) -> List[OpenListSnapshot]:
        """
        Adds to priority queue with heuristic function h(n) but also with actual cost
        function g(n)
        :param new_board:
        :param token_to_test:
        :return:
        """
        children: List[OpenListSnapshot] = []

        if new_board.get_state_stream() not in self.closed_list_set \
                and new_board.get_state_stream() not in self.open_list_set:
            estimate_current_to_finish: int = self.checkered_heuristic(new_board)  # h(n)
            start_to_current: int = self.current_depth + 1  # g(n)
            priority_val: int = estimate_current_to_finish + start_to_current  # f(n)

            new_move_snapshot: MoveSnapshot = MoveSnapshot(token_to_test.get_identifier(),
                                                           new_board.__str__(),
                                                           self.current_depth + 1)
            new_move_snapshot.set_eval(start_to_current, priority_val)
            children.append(OpenListSnapshot(
                new_board,
                new_move_snapshot,
                priority_val
            ))

        return children
