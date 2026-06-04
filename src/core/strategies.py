"""File containing the main strategies (human and AI) for the Tic Tac Toe game."""

import random

from core.board import Board

class Strategy():
    """Base class for move strategies in the Tic Tac Toe game."""
    def get_move(self, board: Board) -> tuple[int, int] | None:
        """Method to be implemented by subclasses to determine the next move."""
        raise NotImplementedError("Subclasses must implement this method.")


class HumanStrategy(Strategy):
    """
    Strategy for a human player, where the move is determined by user input.
    
    Args:
        Strategy (class): The base Strategy class that this strategy inherits from.

    Returns:
        None: The actual move will come from the UI, so this strategy returns None.
    """
    def get_move(self, board: Board) -> None:
        """Get the move from the user interface."""
        return None
    

class RandomAIStrategy(Strategy):
    """
    Strategy for an AI player that selects a random valid move on the board.
    
    Args:
        Strategy (class): The base Strategy class that this strategy inherits from.

    Returns:
        tuple[int, int]: The row and column indices of the selected move.
    """
    def get_move(self, board: Board) -> tuple[int, int] | None:
        """Select a random valid move from the available cells on the board."""
        if not board.get_free_cells():
            return None  # No moves available
        return random.choice(board.get_free_cells())
