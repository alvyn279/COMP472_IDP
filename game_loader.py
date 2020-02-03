from models.game import Game


class GameLoader:
    """
    Parses input file and sets up the game board
    """

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.games = []
        self.__parse_input()

    def __parse_input(self):
        file = open(self.input_file_path, "r")
        lines = file.readlines()

        for line in lines:
            info = line.strip('\n').split(" ")
            self.games.append(Game(*info))

    def get_games(self):
        return self.games
