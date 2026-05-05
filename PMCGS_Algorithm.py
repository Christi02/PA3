import random
from BoardFunctions import (
    get_valid_moves, make_move, undo_move, get_game_result, print_board
)

class MCTSNode:
    def __init__(self):
        self.wi = 0
        self.ni = 0
        self.children = {} # Maps column -> MCTSNode

def run_pmcgs(board, player, mode, param):
    """
    Algorithm 2: Pure Monte Carlo Game Search (PMCGS)
    """
    root = MCTSNode()
    num_simulations = param
    verbose = (mode == "Verbose")
    
    for _ in range(num_simulations):
        curr_node = root
        curr_player = player
        
        path = []
        moves_made = []
        
        while True:
            valid_moves = get_valid_moves(board)
            if not valid_moves:
                break
                
            move = random.choice(valid_moves)
            
            if verbose:
                print(f"wi: {curr_node.wi}")
                print(f"ni: {curr_node.ni}")
                print(f"Move selected: {move + 1}")
                
            if move not in curr_node.children:
                new_node = MCTSNode()
                curr_node.children[move] = new_node
                if verbose:
                    print("NODE ADDED")
                    
                path.append((curr_node, move))
                make_move(board, move, curr_player)
                moves_made.append((move, curr_player))
                
                rollout_player = 'R' if curr_player == 'Y' else 'Y'
                
                while True:
                    result = get_game_result(board)
                    if result is not None:
                        if verbose:
                            print(f"TERMINAL NODE VALUE: {result}")
                        result_value = result
                        break
                        
                    roll_moves = get_valid_moves(board)
                    if not roll_moves:
                        if verbose:
                            print("TERMINAL NODE VALUE: 0")
                        result_value = 0
                        break
                        
                    roll_move = random.choice(roll_moves)
                    if verbose:
                        print(f"Move selected: {roll_move + 1}")
                        
                    make_move(board, roll_move, rollout_player)
                    moves_made.append((roll_move, rollout_player))
                    rollout_player = 'R' if rollout_player == 'Y' else 'Y'
                    
                for p_node, p_move in path:
                    p_node.ni += 1
                    p_node.wi += result_value
                    if verbose:
                        print("Updated values:")
                        print(f"wi: {p_node.wi}")
                        print(f"ni: {p_node.ni}")
                        
                # Undo all moves made during the simulation
                while len(moves_made) > 0:
                    m, p = moves_made.pop()
                    undo_move(board, m)
                    
                break
            else:
                path.append((curr_node, move))
                make_move(board, move, curr_player)
                moves_made.append((move, curr_player))
                
                curr_node = curr_node.children[move]
                curr_player = 'R' if curr_player == 'Y' else 'Y'
                
    # Output expected node performance (except in 'None' mode)
    if mode != "None":
        for c in range(7):
            if c in root.children:
                child = root.children[c]
                val = child.wi / child.ni if child.ni > 0 else 0.0
                print(f"Column {c + 1}: {val:.2f}")
            else:
                print(f"Column {c + 1}: Null")
                
    # Determine the best move based on the player type
    best_move = None
    best_val = -float('inf') if player == 'Y' else float('inf')
    
    for c in range(7):
        if c in root.children:
            child = root.children[c]
            val = child.wi / child.ni if child.ni > 0 else 0.0
            if player == 'Y':
                if val > best_val:
                    best_val = val
                    best_move = c + 1
            else:
                if val < best_val:
                    best_val = val
                    best_move = c + 1
                    
    # Fallback if no children were added
    if best_move is None:
        best_move = random.choice(get_valid_moves(board)) + 1
        
    print(f"FINAL Move selected: {best_move}")
    return best_move
