from game_loader import GameLoader
from models.game import Solver
from strategies.strategies import DepthFirstSearchStrategy


def main():
    print("This is the main execution")

    game_loader = GameLoader("input/sample_input")
    games = game_loader.get_games()

    for game in games:
        game_board = game.get_game_board()
        strategy = DepthFirstSearchStrategy(game.get_max_depth())
        solver = Solver(strategy)

        print(game_board)
        # solver.solve(game_board)


if __name__ == "__main__":
    main()
