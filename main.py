from game_loader import GameLoader
from models.game import Solver
from strategies.strategies import \
    DepthFirstSearchStrategy, \
    BestFirstSearchStrategy,\
    AStarSearchStrategy


def main():
    game_loader = GameLoader("input/sample_input")
    games = game_loader.get_games()

    for game in games:
        game_board = game.get_game_board()
        dfs_strategy = DepthFirstSearchStrategy(game)
        befs_strategy = BestFirstSearchStrategy(game)
        astar_strategy = AStarSearchStrategy(game)

        solver_dfs = Solver(dfs_strategy)
        solver_befs = Solver(befs_strategy)
        solver_astar = Solver(astar_strategy)

        # solver_dfs.solve(game_board)
        solver_befs.solve(game_board)
        solver_astar.solve(game_board)


if __name__ == "__main__":
    main()
