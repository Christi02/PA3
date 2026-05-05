import random

ROWS = 6
COLS = 7

# =========================
# BOARD FUNCTIONS
# =========================

def create_board():
    return [['O' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    for row in board:
        print(''.join(row))
    print()


def is_valid_move(board, col):
    return board[0][col] == 'O'


def get_valid_moves(board):
    return [c for c in range(COLS) if is_valid_move(board, c)]


def make_move(board, col, player):
    for r in reversed(range(ROWS)):
        if board[r][col] == 'O':
            board[r][col] = player
            return r, col
    return None


def undo_move(board, col):
    for r in range(ROWS):
        if board[r][col] != 'O':
            board[r][col] = 'O'
            return


# =========================
# WIN / DRAW DETECTION
# =========================

def check_winner(board, player):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False


def is_draw(board):
    return all(board[0][c] != 'O' for c in range(COLS))


def get_game_result(board):
    if check_winner(board, 'Y'):
        return 1
    if check_winner(board, 'R'):
        return -1
    if is_draw(board):
        return 0
    return None


# =========================
# FILE READER
# =========================

def load_board_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    algorithm = lines[0]
    player = lines[1]
    board_lines = lines[2:8]

    board = [list(row.replace('0', 'O')) for row in board_lines]

    return algorithm, player, board
