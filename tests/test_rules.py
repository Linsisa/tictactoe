"""File of tests for the rules and logic of the Tic Tac Toe game."""

import pytest
import core.rules as rules

from core.board import Board
from config.settings import BOARD_SIZE_TEST


class TestRules:
    """Test class for the rules and logic of the Tic Tac Toe game."""

    ### Tests for check_winner function ###
    @pytest.mark.parametrize("board_state, last_move, expected_winner", [
        # Horizontal win
        ([['X', 'X', 'X'], 
          ['O', 'O', None], 
          [None, None, None]], (0, 0), 'X'), # Left
        ([['X', 'X', 'X'], 
          ['O', 'O', None], 
          [None, None, None]], (0, 1), 'X'), # Middle
        ([['X', 'X', 'X'], 
          ['O', 'O', None],
          [None, None, None]], (0, 2), 'X'), # Right
        # Vertical win
        ([['X', 'O', None],
          ['X', 'O', None], 
          ['X', None, None]], (0, 0), 'X'), # Top
        ([['X', 'O', None], 
          ['X', 'O', None], 
          ['X', None, None]], (1, 0), 'X'), # Middle
        ([['X', 'O', None], 
          ['X', 'O', None], 
          ['X', None, None]], (2, 0), 'X'), # Bottom
        # Main diagonal win
        ([['X', 'O', None], 
          ['O', 'X', None], 
          [None, None, 'X']], (0, 0), 'X'), # Top-left
        ([['X', 'O', None], 
          ['O', 'X', None], 
          [None, None, 'X']], (1, 1), 'X'), # Center
        ([['X', 'O', None], 
          ['O', 'X', None], 
          [None, None, 'X']], (2, 2), 'X'), # Bottom-right
        # Anti-diagonal win
        ([[None, 'O', 'X'], 
          ['O', 'X', None], 
          ['X', None, None]], (0, 2), 'X'), # Top-right
        ([[None, 'O', 'X'], 
          ['O', 'X', None], 
          ['X', None, None]], (1, 1), 'X'), # Center
        ([[None, 'O', 'X'], 
          ['O', 'X', None], 
          ['X', None, None]], (2, 0), 'X'), # Bottom-left
        # No winner
        ([['X', 'O', 'X'], 
          ['O', 'X', 'O'], 
          ['O', 'X', 'O']], (1, 1), None), # Full
    ])
    def test_check_winner_scenarios(self, board_state, last_move, expected_winner):
        """Test the check_winner function with various board states and last moves."""
        win_length = 3
        self.board = Board(size=BOARD_SIZE_TEST)
        self.board.set_board(board_state)  # Set the board to the desired state for the test 

        result = rules.check_winner(self.board, last_move, win_length)
        assert result == expected_winner


    def test_check_winner_win_length_greater_than_board_size(self):
        """Test the check_winner function when the win length is greater than the board size."""
        board_state = [['X', 'O', None], 
                       ['O', 'X', None], 
                       [None, None, 'X']]
        last_move = (1, 1)
        win_length = 4  # Greater than board size

        self.board = Board(size=BOARD_SIZE_TEST)
        self.board.set_board(board_state)

        result = rules.check_winner(self.board, last_move, win_length)
        assert result is None  # No winner should be detected

    def test_check_winner_win_length_lower_than_board_size(self):
        """Test the check_winner function when the win length is lower than the board size."""
        board_state = [['X', 'X', None], 
                       ['O', None, None], 
                       [None, None, 'O']]
        last_move = (0, 1)
        win_length = 2  # Lower than board size

        self.board = Board(size=BOARD_SIZE_TEST)
        self.board.set_board(board_state)

        expected_winner = 'X'  # 'X' has two in a row horizontally at the top row
        result = rules.check_winner(self.board, last_move, win_length)
        assert result == expected_winner  # Winner should be detected


    ### Tests for check_draw function ###
    @pytest.mark.parametrize("board_state, last_move, expected_draw", [
        # Full board with no winner (draw)
        ([['X', 'O', 'X'], 
          ['O', 'X', 'O'], 
          ['O', 'X', 'O']], (1, 1), True), # Full
        # Full board but not a draw (winner present)
        ([['X', 'X', 'X'], 
          ['O', 'O', 'X'], 
          ['X', 'X', 'O']], (0, 0), False), # Winner present
        # Not a draw (empty cells)
        ([['X', 'O', 'X'], 
          ['O', None, 'O'], 
          ['O', 'X', 'O']], (1, 2), False), # One empty cell
        # Not a draw (winner present)
        ([['X', 'X', 'X'], 
          ['O', 'O', None], 
          [None, None, None]], (0, 0), False), # Winner present
    ])
    def test_check_draw_scenarios(self, board_state, last_move, expected_draw):
        """Test the check_draw function with various board states and last moves."""
        win_length = 3
        self.board = Board(size=BOARD_SIZE_TEST)
        self.board.set_board(board_state)  # Set the board to the desired state for the test 

        result = rules.check_draw(self.board, last_move, win_length)
        assert result == expected_draw
