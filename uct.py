import math
import random
from BoardFunctions import get_valid_moves, make_move, undo_move, get_game_result
from tree_node import TreeNode

# exploration constant; standard value from R&N
C = math.sqrt(2)

def other_player(player):
    # simple helper to alternate turns
    return 'Y' if player == 'R' else 'R'

def ucb_value(node, parent_ni, is_maximizing):
    # UCB formula: wi/ni + c * sqrt(log(N) / ni)
    if node.ni == 0:
        # unvisited nodes get infinite priority so they get explored first
        return float('inf') if is_maximizing else float('-inf')
    exploitation = node.wi / node.ni
    exploration = C * math.sqrt(math.log(parent_ni) / node.ni)
    if is_maximizing:
        return exploitation + exploration
    else:
        return exploitation - exploration

def run_simulation(root, board, current_player, mode):
    # PHASE 1: SELECTION
    # walk down existing tree using UCB until we find an expandable node
    node = root
    path = [node]  # track nodes visited for backprop later
    player = current_player

    while True:
        valid_moves = get_valid_moves(board)
        result = get_game_result(board)

        # if terminal state, stop selecting
        if result is not None:
            break

        # check if any valid move is unexplored
        unexplored = [m for m in valid_moves if m not in node.children]

        if unexplored:
            # PHASE 2: EXPANSION
            col = random.choice(unexplored)
            make_move(board, col, player)
            new_node = TreeNode(parent=node)
            node.children[col] = new_node
            path.append(new_node)
            if mode == "Verbose":
                print("NODE ADDED")
                print(f"Move selected: {col + 1}")  # convert to 1-indexed
            player = other_player(player)
            node = new_node
            break
        else:
            # all children exist; use UCB to select best child
            is_maximizing = (player == 'Y')
            best_col = None
            best_val = float('-inf') if is_maximizing else float('inf')

            if mode == "Verbose":
                # print wi/ni for current node before UCB values
                print(f"wi: {int(node.wi)}")
                print(f"ni: {node.ni}")
                # print UCB values for all 7 columns
                for c in range(7):
                    if c in node.children:
                        v = ucb_value(node.children[c], node.ni, is_maximizing)
                        print(f"V{c+1}: {v:.2f}")

            for col in valid_moves:
                child = node.children[col]
                val = ucb_value(child, node.ni, is_maximizing)
                if is_maximizing and val > best_val:
                    best_val = val
                    best_col = col
                elif not is_maximizing and val < best_val:
                    best_val = val
                    best_col = col

            if mode == "Verbose":
                print(f"Move selected: {best_col + 1}")

            make_move(board, best_col, player)
            path.append(node.children[best_col])
            node = node.children[best_col]
            player = other_player(player)

    # PHASE 3: ROLLOUT
    # play randomly until terminal state
    rollout_moves = []
    result = get_game_result(board)

    while result is None:
        valid_moves = get_valid_moves(board)
        col = random.choice(valid_moves)
        make_move(board, col, player)
        rollout_moves.append(col)
        if mode == "Verbose":
            print(f"Move selected: {col + 1}")
        player = other_player(player)
        result = get_game_result(board)

    if mode == "Verbose":
        print(f"TERMINAL NODE VALUE: {result}")

    # PHASE 4: BACKPROPAGATION
    # undo rollout moves to restore board state
    for col in reversed(rollout_moves):
        undo_move(board, col)

    # update wi and ni for every node on the path
    for visited_node in reversed(path):
        visited_node.ni += 1
        visited_node.wi += result
        if mode == "Verbose":
            print("Updated values:")
            print(f"wi: {int(visited_node.wi)}")
            print(f"ni: {visited_node.ni}")


def uct(board, player, num_simulations, mode):
    root = TreeNode()
    valid_moves = get_valid_moves(board)

    # track which moves were made going into the tree for undo purposes
    # we rebuild this by tracking cols separately
    for _ in range(num_simulations):
        # we need to track moves made so we can undo them after each simulation
        sim_board = [row[:] for row in board]  # copy board per simulation
        run_simulation(root, sim_board, player, mode)

    # FINAL MOVE SELECTION
    # pick best child by wi/ni only; no exploration bonus
    is_maximizing = (player == 'Y')
    best_col = None
    best_val = float('-inf') if is_maximizing else float('inf')

    for col in range(7):
        if col in root.children:
            child = root.children[col]
            val = child.wi / child.ni
            print(f"Column {col+1}: {round(val, 2)}")
        else:
            print(f"Column {col+1}: Null")

    for col in valid_moves:
        if col in root.children:
            child = root.children[col]
            val = child.wi / child.ni
            if is_maximizing and val > best_val:
                best_val = val
                best_col = col
            elif not is_maximizing and val < best_val:
                best_val = val
                best_col = col

    print(f"FINAL Move selected: {best_col + 1}")
    return best_col