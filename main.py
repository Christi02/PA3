import sys
from BoardFunctions import load_board_from_file
from UR_Algorithm import run_ur
from PMCGS_Algorithm import run_pmcgs

def main():
    if len(sys.argv) != 4:
        print("Usage: python program.py <input_file> <Verbose|Brief|None> <param>")
        return

    filename = sys.argv[1]
    mode = sys.argv[2]
    param = int(sys.argv[3])

    algorithm, player, board = load_board_from_file(filename)

    # Placeholder for algorithms (to be implemented by teammates)
    if algorithm == "UR":
        run_ur(board, player, mode, param)
    elif algorithm == "PMCGS":
        run_pmcgs(board, player, mode, param)    elif algorithm == "UCT":
    else:
        print("Unknown algorithm.")


if __name__ == "__main__":
    main()
