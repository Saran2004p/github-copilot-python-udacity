import pytest


def test_create_empty_board_shape_and_empty(sudoku_logic_module):
    board = sudoku_logic_module.create_empty_board()
    assert len(board) == sudoku_logic_module.SIZE
    assert all(len(row) == sudoku_logic_module.SIZE for row in board)
    # All cells should be EMPTY
    assert all(cell == sudoku_logic_module.EMPTY for row in board for cell in row)


def test_is_safe_basic(sudoku_logic_module):
    board = sudoku_logic_module.create_empty_board()
    # place a number and ensure conflicts are detected
    board[0][0] = 5
    assert not sudoku_logic_module.is_safe(board, 0, 1, 5)  # same row
    assert not sudoku_logic_module.is_safe(board, 1, 0, 5)  # same column
    assert not sudoku_logic_module.is_safe(board, 1, 1, 5)  # same 3x3 box
    assert sudoku_logic_module.is_safe(board, 4, 4, 5)  # no conflict far away


def test_generate_puzzle_and_solution_contents(sudoku_logic_module):
    puzzle, solution = sudoku_logic_module.generate_puzzle(clues=30)
    # shapes
    assert len(puzzle) == sudoku_logic_module.SIZE
    assert len(solution) == sudoku_logic_module.SIZE
    assert all(len(row) == sudoku_logic_module.SIZE for row in puzzle)
    assert all(len(row) == sudoku_logic_module.SIZE for row in solution)
    # solution should be fully filled (no EMPTY cells)
    assert all(cell != sudoku_logic_module.EMPTY for row in solution for cell in row)
    # puzzle should have at least one EMPTY cell (unless clues==81)
    assert any(cell == sudoku_logic_module.EMPTY for row in puzzle for cell in row)
