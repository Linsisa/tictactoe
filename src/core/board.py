"""Board implementation for the Tic Tac Toe game."""

from config.settings import BOARD_SIZE, EMPTY_CELL

class Board:
    """Class representing the game board for Tic Tac Toe."""

    def __init__(self):
        """Initialize the game board with empty cells."""
        self.board: list[list[str | None]] = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def reset_board(self):
        """Reset the game board to its initial empty state."""
        self.board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def make_move(self, row: int, col: int, symbol: str) -> bool:
        """
        Place a symbol on the board at the specified position.

        Args:
            row (int): The row index where the symbol should be placed.
            col (int): The column index where the symbol should be placed.
            symbol (str): The symbol to place on the board (e.g., 'X' or 'O').

        Returns:
            bool: True if the move was successful, False if the cell is already occupied.
        """

        if self.board[row][col] == EMPTY_CELL:
            self.board[row][col] = symbol
            return True
        return False

    def get_board_state(self):
        """Return the current state of the board."""
        return self.board
    
    def get_free_cells(self):
        """Return a list of free cells on the board."""
        return [(row_idx, col_idx) 
                for row_idx in range(len(self.board)) 
                for col_idx in range(len(self.board[row_idx])) 
                if self.board[row_idx][col_idx] == EMPTY_CELL]
    
    def is_full(self) -> bool:
        """Check if the board is full (no free cells)."""
        isFull = False if self.get_free_cells() else True
        return isFull

        