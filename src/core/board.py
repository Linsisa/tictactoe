"""Board implementation for the Tic Tac Toe game."""

from config.settings import EMPTY_CELL


class Board:
    """Class representing the game board for Tic Tac Toe."""

    def __init__(self, size: int):
        """Initialize the game board with empty cells."""
        self.size = size
        self.reset_board()

    def reset_board(self):
        """Reset the game board to its initial empty state."""
        self.board: list[list[str | None]] = [[EMPTY_CELL for _ in range(self.size)] for _ in range(self.size)]
    
    def set_board(self, new_board: list[list[str | None]]):
        """Set the board to a new state (used for testing purposes)."""
        self.board = new_board

    def apply_move(self, move: tuple[int, int], symbol: str) -> bool:
        """
        Place a symbol on the board at the specified position.

        Args:
            move (tuple[int, int]): The row and column indices for the move.
            symbol (str): The symbol to place on the board (e.g., 'X' or 'O').

        Returns:
            bool: True if the move was successful, False if the cell is already occupied or the position is out of bounds.
        """
        row, col = move

        if self.is_position_in_bounds(move) and self.board[row][col] == EMPTY_CELL:
            self.board[row][col] = symbol
            return True
        return False

    def get_current_board(self):
        """Return the current state of the board."""
        return [row.copy() for row in self.board]
    
    def get_cell(self, row: int, col: int) -> str | None:
        """Return the value of a specific cell on the board."""
        return self.board[row][col]
    
    def get_free_cells(self):
        """Return a list of free cells on the board."""
        return [(row_idx, col_idx) 
                for row_idx in range(len(self.board)) 
                for col_idx in range(len(self.board[row_idx])) 
                if self.board[row_idx][col_idx] == EMPTY_CELL]
    
    def is_full(self) -> bool:
        """Check if the board is full (no free cells)."""
        return not self.get_free_cells()
    
    def is_position_in_bounds(self, position: tuple[int, int]) -> bool:
        """Check if a given position is within the bounds of the board."""
        row, col = position
        return 0 <= row < self.size and 0 <= col < self.size
