"""Player class representing a player in the Tic Tac Toe game."""

from dataclasses import dataclass
from core.strategies import Strategy


@dataclass
class Player:
    name: str
    symbol: str
    strategy: Strategy

    def get_move(self, board: "Board", position: tuple[int, int] = None) -> tuple[int, int] | None:
        """
        Return the move for the player based on their strategy.

        Args:
            board (Board): The current state of the game board.

        Returns:
            tuple[int, int] | None: The row and column indices of the move.      
        """
        return self.strategy.get_move(board, position)