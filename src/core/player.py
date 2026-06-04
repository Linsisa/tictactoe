"""Player class representing a player in the Tic Tac Toe game."""

from dataclasses import dataclass
from core.strategies import Strategy


@dataclass
class Player:
    name: str
    symbol: str
    strategy: Strategy

    def get_move(self, board: "Board") -> tuple[int, int] | None:
        """
        Get the player's move based on their strategy.

        Args:
            board (Board): The current state of the game board.

        Returns:
            tuple[int, int] | None: The row and column indices in case of AI playing
                                    else "None" player move come from UI.        
        """
        return self.strategy.get_move(board)