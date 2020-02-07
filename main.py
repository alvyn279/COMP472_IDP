from game_loader import GameLoader
from models.game import Solver
from strategies.strategies import DepthFirstSearchStrategy


def main():
    game_loader = GameLoader("input/sample_input")
    games = game_loader.get_games()

    for game in games:
        game_board = game.get_game_board()
        dfs_strategy = DepthFirstSearchStrategy(game)
        solver = Solver(dfs_strategy)

        solver.solve(game_board)


if __name__ == "__main__":
    main()
