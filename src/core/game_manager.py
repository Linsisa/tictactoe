"""File of the GameManager class, which manages the overall game flow and state for the Tic Tac Toe game."""

from config.settings import SYMBOL_X
from core.board import Board
from core.player import Player
from core.rules import check_winner, check_draw


class GameManager:
    """Class responsible for managing the game flow and state of the Tic Tac Toe game."""

    def __init__(self, player1: Player, player2: Player, board_size: int, win_length: int):
        """
        Initialize the GameManager with two players, a game board, and win conditions.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
            board_size (int): The size of the game board (e.g., 3 for a 3x3 board).
            win_length (int): The number of consecutive symbols needed to win (e.g., 3 for standard Tic Tac Toe).
        """
        self.players = [player1, player2]
        self._board = Board(board_size)
        self._win_length = win_length
        self._current_player_index = self._define_starting_player()
        self._winner: Player | None = None
        self.game_over = False
        self._last_move: tuple[int, int] | None = None

        if self._win_length > self._board.size:
            raise ValueError(f"win_length ({self._win_length}) cannot exceed board_size ({self._board.size})")

    def reset_game(self):
        """Reset the game to its initial state."""
        self._board.reset_board()
        self._current_player_index = self._define_starting_player()
        self._winner = None
        self.game_over = False
        self._last_move = None

    def play_turn(self, position: tuple[int, int] | None = None) -> bool:
        """
        Play a turn for the current player.
        - If the current player is human, `position` should be provided by the UI.
        - If it's the AI, `position` can be None and will be chosen by the strategy.

        Args:
            position (tuple[int, int] | None): The row and column indices for the move, or None for AI.

        Returns:
            bool: True if the player move was played, False otherwise.
        """
        # Stop if the game is over, no more moves can be played.
        if self.game_over:
            return False

        player = self.get_current_player()
        move = player.get_move(self._board, position)
        
        # After move is selected, apply it to the board.
        success = self._board.apply_move(move, player.symbol) if move is not None else False
        if not success:
            return False

        # If the move was successful, we update the last move and check for win/draw conditions.
        self._last_move = move
        self._after_turn()
        return True
        
    def _after_turn(self) -> None:
        """Method to be called after each turn to update the game state, check for win/draw conditions."""
        if self._last_move is None:
            return

        # Check whether the last move created a winner.
        winner_symbol = check_winner(self._board, self._last_move, self._win_length)
        if winner_symbol:
            self._winner = self.get_current_player()
            self.game_over = True
            return
        
        # If there is no winner, check for a draw.
        if check_draw(self._board, self._last_move, self._win_length):
            self.game_over = True
            return
        
        # Reaching this point means the game is not over, so we switch to the next player.
        self._switch_player()

    def get_current_board_state(self) -> list[list[str | None]]:
        """Return the current state of the board as a 2D list."""
        return self._board.get_current_board()
    
    def get_board_cell(self, row: int, col: int) -> str | None:
        """Return the value of a specific cell on the board."""
        return self._board.get_cell(row, col)
    
    def _set_board(self, new_board: list[list[str | None]]) -> None:
        """Set the board to a new state (used for testing purposes)."""
        self._board.set_board(new_board)
    
    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.players[self._current_player_index]
    
    def get_current_player_index(self) -> int:
        """Return the index of the current player (0 or 1)."""
        return self._current_player_index
    
    def is_human_input_allowed(self) -> bool:
        """Determine if human input is allowed based on the current game state and player type."""
        return not self.game_over and self.players[self._current_player_index].strategy.is_human

    def is_game_over(self) -> bool:
        """Return True if the game is over, False otherwise."""
        return self.game_over
    
    def get_winner(self) -> Player | None:
        """Return the winner of the game, or None if there is no winner."""
        return self._winner
    
    def _set_winner(self, player_index: int) -> None:
        """Set the winner of the game (used for testing purposes)."""
        self._winner = self.players[player_index]

    def get_last_move(self) -> tuple[int, int] | None:
        """Return the last move made in the game, or None if no moves have been made."""
        return self._last_move
    
    def _set_last_move(self, move: tuple[int, int]) -> None:
        """Set the last move made in the game (used for testing purposes)."""
        self._last_move = move

    def _switch_player(self) -> None:
        """Switch the current player to the other player."""
        self._current_player_index = 1 - self._current_player_index

    def _define_starting_player(self) -> int:
        """Select the player with the 'X' symbol as the starting player."""
        starting_player = 0 if self.players[0].symbol == SYMBOL_X else 1
        return starting_player
