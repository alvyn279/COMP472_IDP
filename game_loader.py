from models.game import Game


class GameLoader:
    """
    Parses input file and sets up the games
    """

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.games = []
        self.__parse_input()

    def __parse_input(self):
        file = open(self.input_file_path, "r")
        lines = file.readlines()

        for index, line in enumerate(lines):
            info = line.strip('\n').split(" ")
            parseable_info = [int(info[0]), int(info[1]), int(info[2]), info[3], index]
            self.games.append(Game(*parseable_info))

    def get_games(self):
        return self.games
