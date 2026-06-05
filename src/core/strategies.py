"""File containing the main strategies (human and AI) for the Tic Tac Toe game."""

import random

from abc import ABC, abstractmethod
from core.board import Board

class Strategy(ABC):
    """Base class for move strategies in the Tic Tac Toe game."""
    is_human: bool = False

    @abstractmethod
    def get_move(self, board: Board) -> tuple[int, int] | None:
        """Method to be implemented by subclasses to determine the next move."""
        raise NotImplementedError("Subclasses must implement this method.")


class HumanStrategy(Strategy):
    """
    Strategy for a human player. Returns None; move is handled by UI.

    Returns:
        None: The actual move will come from the UI, so this strategy returns None.
    """
    is_human: bool = True

    def get_move(self, board: Board) -> tuple[int, int] | None:
        """Get the move from the user interface."""
        return None
    

class RandomAIStrategy(Strategy):
    """
    Strategy for an AI player that selects a random valid move on the board.
    
    Returns:
        tuple[int, int]: The row and column indices of the selected move.
    """
    def get_move(self, board: Board) -> tuple[int, int] | None:
        """Select a random valid move from the available cells on the board."""
        free_cells = board.get_free_cells()

        if not free_cells:
            return None  # No moves available
        return random.choice(free_cells)
