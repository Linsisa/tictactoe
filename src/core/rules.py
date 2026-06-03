"""File containing the rules and logic for the Tic Tac Toe game."""


from core.board import Board


def check_winner(board: Board, last_move: tuple[int, int], win_length: int) -> str | None:
    """
    Check to see if there is a winner by looking for the winning pattern in the row, column, and diagonals of the last move.
    
    Args:
        board (Board): The current state of the game board.
        last_move (tuple[int, int]): The position of the last move made.
        win_length (int): The number of consecutive symbols needed to win.

    Returns:
        str | None: The symbol of the winning player, or None if there is no winner.
    """
    if not board.is_position_in_bounds(last_move):
        return None

    if check_horizontal_win(board, last_move, win_length) or \
        check_vertical_win(board, last_move, win_length) or \
        check_main_diagonal_win(board, last_move, win_length) or \
        check_anti_diagonal_win(board, last_move, win_length):
        return board.get_cell(*last_move)

    return None


def check_draw(board: Board, last_move: tuple[int, int], win_length: int) -> bool:
    """
    Check if the game is a draw (no winner and no free cells).
    
    Args:
        board (Board): The current state of the game board.
        last_move (tuple[int, int]): The position of the last move made.
        win_length (int): The number of consecutive symbols needed to win.

    Returns:
        bool: True if the game is a draw, False otherwise.
    """
    return board.is_full() and check_winner(board, last_move, win_length) is None


### Helper functions for rules.py ###
def check_direction(board: Board, last_move: tuple[int, int], win_length: int, dx: int, dy: int) -> bool:
    """
    Check if there is a continuous sequence (size >= win_length) 
    in a specific direction (defined by dx and dy) of the symbol 
    present in cell from the last move.
    
    Args:
        board (Board): The current state of the game board.
        last_move (tuple[int, int]): The position of the last move made.
        win_length (int): The number of consecutive symbols needed to win.
        dx (int): The change in row index for each step in the direction.
        dy (int): The change in column index for each step in the direction.

    Returns:
        bool: True if there is a winning sequence in the specified direction, False otherwise.
    """
    symbol = board.get_cell(*last_move) # Get last player symbol from the last move position
    count = 1  # Start with 1 to include the last move itself
    row, col = last_move

    # Check in the positive direction (dx, dy)
    i, j = row + dx, col + dy
    while board.is_position_in_bounds((i, j)) and board.get_cell(i, j) == symbol:
        count += 1
        i += dx
        j += dy

    # Check in the negative direction (-dx, -dy)
    i, j = row - dx, col - dy
    while board.is_position_in_bounds((i, j)) and board.get_cell(i, j) == symbol:
        count += 1
        i -= dx
        j -= dy

    return count >= win_length


def check_horizontal_win(board: Board, symbol: str, last_move: tuple[int, int], win_length: int) -> bool:
    """Check if there is a winning sequence of the given symbol in horizontal directions from the last move."""
    return check_direction(board, symbol, last_move, win_length, dx=0, dy=1)


def check_vertical_win(board: Board, symbol: str, last_move: tuple[int, int], win_length: int) -> bool:
    """Check if there is a winning sequence of the given symbol in vertical directions from the last move."""
    return check_direction(board, symbol, last_move, win_length, dx=1, dy=0)


def check_main_diagonal_win(board: Board, symbol: str, last_move: tuple[int, int], win_length: int) -> bool:
    """Check if there is a winning sequence of the given symbol in the main diagonal direction from the last move."""
    return check_direction(board, symbol, last_move, win_length, dx=1, dy=1)


def check_anti_diagonal_win(board: Board, symbol: str, last_move: tuple[int, int], win_length: int) -> bool:
    """Check if there is a winning sequence of the given symbol in the bottom-left to top-right diagonal direction from the last move."""
    return check_direction(board, symbol, last_move, win_length, dx=1, dy=-1)
