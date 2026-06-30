import copy
import random

SIZE = 9
EMPTY = 0


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


# Solver utilities used to check uniqueness of solutions
def _find_empty(board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY:
                return i, j
    return None


def _solve_count(board, limit=2):
    """Count number of solutions for the given board up to `limit`.
    Uses backtracking and stops early if count reaches limit.
    """
    loc = _find_empty(board)
    if loc is None:
        return 1
    row, col = loc
    count = 0
    for num in range(1, SIZE + 1):
        if is_safe(board, row, col, num):
            board[row][col] = num
            count += _solve_count(board, limit)
            board[row][col] = EMPTY
            if count >= limit:
                return count
    return count


def remove_cells(board, clues):
    """
    Remove cells from a full board while preserving a unique solution.
    Attempts to remove (SIZE*SIZE - clues) cells. If removing a specific cell would
    result in multiple solutions, it is restored.
    """
    attempts = SIZE * SIZE - clues
    # Work from a randomized list of positions so puzzles vary
    cells = [(r, c) for r in range(SIZE) for c in range(SIZE)]
    random.shuffle(cells)
    removed = 0

    for (row, col) in cells:
        if removed >= attempts:
            break
        if board[row][col] == EMPTY:
            continue
        backup = board[row][col]
        board[row][col] = EMPTY

        # Check uniqueness: make a copy and count solutions up to 2
        board_copy = deep_copy(board)
        count = _solve_count(board_copy, limit=2)

        if count != 1:
            # Not unique, restore the value
            board[row][col] = backup
        else:
            removed += 1

    # If we couldn't remove as many cells as requested (due to uniqueness constraints),
    # that's acceptable — the puzzle will simply have more clues.


def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
