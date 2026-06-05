"""File of tests for the strategies used in the Tic Tac Toe game."""

import pytest

from config.test_settings import BOARD_SIZE_TEST
from core.board import Board
from core.strategies import Strategy, HumanStrategy, RandomAIStrategy

class TestStrategies:
    """Test class for the strategies available in the game."""

    def setup_method(self):
        """Set up a new board instance before each test."""
        self.board = Board(size=BOARD_SIZE_TEST)

    def test_base_strategy_raises_not_implemented(self):
        """Test that the base strategy raises NotImplementedError."""
        strategy = Strategy()
        with pytest.raises(NotImplementedError):
            strategy.get_move(self.board)

    def test_human_strategy_returns_none(self):
        """Test that the human strategy returns None."""
        strategy = HumanStrategy()
        assert strategy.get_move(self.board) is None

    def test_random_ai_strategy_picks_valid_cell(self):
        """Test that the random AI strategy picks a valid cell."""
        strategy = RandomAIStrategy()
        
        self.board.set_board(
            [['X', 'O', None],
             [None, 'X', 'O'],
             ['O', None, 'X']]
        )
        free_cells = self.board.get_free_cells()
        

        ai_chosen_move = strategy.get_move(self.board)
        
        # Le coup doit être dans la liste des cases libres
        assert ai_chosen_move in free_cells

    def test_random_ai_strategy_only_one_choice_left(self):
        """Test that the random AI strategy picks the only remaining cell if the board is almost full."""
        strategy = RandomAIStrategy()
        
        # Il ne reste que la case centrale (1, 1) de libre
        self.board.set_board(
            [['X', 'O', 'X'],
             ['O', None, 'O'],
             ['O', 'X', 'X']]
        )
        
        ai_chosen_move = strategy.get_move(self.board)
        assert ai_chosen_move == (1, 1)

    def test_random_ai_strategy_no_moves_left(self):
        """Test that the random AI strategy returns None if there are no free cells left."""
        strategy = RandomAIStrategy()
        
        # Le plateau est plein, il n'y a plus de cases libres
        self.board.set_board(
            [['X', 'O', 'X'],
             ['O', 'X', 'O'],
             ['O', 'X', 'O']]
        )
        
        ai_chosen_move = strategy.get_move(self.board)
        assert ai_chosen_move is None