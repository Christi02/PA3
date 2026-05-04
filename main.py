import sys
from BoardFunctions import load_board_from_file

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
        print("UR algorithm not implemented yet.")
    elif algorithm == "PMCGS":
        print("PMCGS algorithm not implemented yet.")
    elif algorithm == "UCT":
        print("UCT algorithm not implemented yet.")
    else:
        print("Unknown algorithm.")


if __name__ == "__main__":
    main()