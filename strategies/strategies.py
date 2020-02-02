# algorithms as strategies

from abc import ABC, abstractmethod


class SearchStrategy(ABC):
    """
    Strategy interface for the different algorithms that will be used
    to solve Indonesian Dot Puzzle
    """

    @abstractmethod
    def execute(self,):
        pass
