from abc import ABC, abstractmethod
from models.game import Board


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
    """

    def __init__(self, max_depth):
        self.max_depth = max_depth

    def execute(self, initial_board: Board):
        # implement DFS
        pass
