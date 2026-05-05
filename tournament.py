# Round-robin tournament runner for PA3
# Runs 100 games per matchup between 5 algorithm configurations
from BoardFunctions import create_board, make_move, get_game_result, get_valid_moves
from uct import uct, other_player
from algorithms import ur, pmcgs

# ================================================
# PLUG IN YAHIR'S CODE HERE
# import ur and pmcgs from his file once pushed
# from algorithms import ur, pmcgs
# ================================================

def get_move(board, player, algorithm, param, mode="None"):
    # routes to correct algorithm based on name
    if algorithm == "UR":
        # ================================================
        # YAHIR'S UR FUNCTION GOES HERE
        # return ur(board, player)
        # ================================================
        return ur(board, player)
    elif algorithm == "PMCGS":
        # ================================================
        # YAHIR'S PMCGS FUNCTION GOES HERE
        # return pmcgs(board, player, param, mode)
        # ================================================
        return pmcgs(board, player, param, mode)
    elif algorithm == "UCT":
        return uct(board, player, param, mode)

def play_game(algo1, param1, algo2, param2):
    # plays one full game between two algorithms
    # algo1 starts as Yellow (Max), algo2 starts as Red (Min)
    board = create_board()
    # Yellow always goes first per Connect Four rules
    current_player = 'Y'
    current_algo = algo1
    current_param = param1

    while True:
        result = get_game_result(board)
        if result is not None:
            return result  # 1 = Yellow wins, -1 = Red wins, 0 = draw

        col = get_move(board, current_player, current_algo, current_param)
        make_move(board, col, current_player)

        # alternate player and algorithm
        if current_player == 'Y':
            current_player = 'R'
            current_algo = algo2
            current_param = param2
        else:
            current_player = 'Y'
            current_algo = algo1
            current_param = param1

def run_tournament():
    # 5 algorithm configurations per PA3 spec
    algorithms = [
        ("UR", 0),
        ("PMCGS", 500),
        ("PMCGS", 10000),
        ("UCT", 500),
        ("UCT", 10000),
    ]

    labels = ["UR", "PMCGS(500)", "PMCGS(10000)", "UCT(500)", "UCT(10000)"]
    num_games = 100
    # results[i][j] = wins for algorithm i against algorithm j
    results = [[0] * 5 for _ in range(5)]

    for i in range(5):
        for j in range(5):
            algo1, param1 = algorithms[i]
            algo2, param2 = algorithms[j]
            wins = 0

            # 50 games: algo1 = Yellow, algo2 = Red
            for _ in range(num_games // 2):
                result = play_game(algo1, param1, algo2, param2)
                if result == 1:  # Yellow wins = algo1 wins
                    wins += 1
                elif result == 0:
                    wins += 0.5  # count draws as half a win

            # 50 games: algo2 = Yellow, algo1 = Red
            for _ in range(num_games // 2):
                result = play_game(algo2, param2, algo1, param1)
                if result == -1:  # Red wins = algo1 wins
                    wins += 1
                elif result == 0:
                    wins += 0.5

            results[i][j] = round((wins / num_games) * 100, 1)
            print(f"Done: {labels[i]} vs {labels[j]} -> {results[i][j]}%")

    # print final results table
    print("\n===== TOURNAMENT RESULTS (Win % for row vs column) =====\n")
    header = f"{'':15}" + "".join(f"{l:15}" for l in labels)
    print(header)
    for i in range(5):
        row = f"{labels[i]:15}" + "".join(f"{results[i][j]:15}" for j in range(5))
        print(row)

if __name__ == "__main__":
    run_tournament()
