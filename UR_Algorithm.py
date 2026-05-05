import random
from BoardFunctions import get_valid_moves

def run_ur(board, player, mode, param):
    """
    Algorithm 1: Uniform Random (UR)
    """
    valid_moves = get_valid_moves(board)
    if not valid_moves:
        print("No valid moves available.")
        return None
    
    selected_col = random.choice(valid_moves)
    
    print(f"FINAL Move selected: {selected_col + 1}")
    return selected_col + 1
