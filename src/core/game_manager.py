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
        self.board = Board(board_size)
        self.win_length = win_length
        self.current_player_index = self._define_starting_player()
        self.winner: Player | None = None
        self.game_over = False
        self.last_move: tuple[int, int] | None = None

        if self.win_length > self.board.size:
            raise ValueError(f"win_length ({self.win_length}) cannot exceed board_size ({self.board.size})")

    def reset_game(self):
        """Reset the game to its initial state."""
        self.board.reset_board()
        self.current_player_index = self._define_starting_player()
        self.winner = None
        self.game_over = False
        self.last_move = None

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
        move = self._get_move_for_player(player, position)
        
        # After move is selected, apply it to the board.
        success = self.board.apply_move(move, player.symbol) if move is not None else False
        if not success:
            return False

        # If the move was successful, we update the last move and check for win/draw conditions.
        self.last_move = move
        self._after_turn()
        return True
        
    def _after_turn(self) -> None:
        """Method to be called after each turn to update the game state, check for win/draw conditions."""
        if self.last_move is None:
            return

        # Check whether the last move created a winner.
        winner_symbol = check_winner(self.board, self.last_move, self.win_length)
        if winner_symbol:
            self.winner = self.get_current_player()
            self.game_over = True
            return
        
        # If there is no winner, check for a draw.
        if check_draw(self.board, self.last_move, self.win_length):
            self.game_over = True
            return
        
        # Reaching this point means the game is not over, so we switch to the next player.
        self._switch_player()

    def get_current_board_state(self) -> list[list[str | None]]:
        """Return the current state of the board as a 2D list."""
        return self.board.get_current_board()
    
    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.players[self.current_player_index]
    
    def is_current_player_human(self) -> bool:
        """Return True if the current player is a human player, False otherwise."""
        player = self.get_current_player()
        return player.strategy.is_human
    
    def is_human_input_allowed(self) -> bool:
        """Determine if human input is allowed based on the current game state and player type."""
        return not self.game_over and self.is_current_player_human()

    def _switch_player(self) -> None:
        """Switch the current player to the other player."""
        self.current_player_index = 1 - self.current_player_index

    def _define_starting_player(self) -> int:
        """Select the player with the 'X' symbol as the starting player."""
        starting_player = 0 if self.players[0].symbol == SYMBOL_X else 1
        return starting_player

    def _get_move_for_player(self, player: Player, position: tuple[int, int] | None) -> tuple[int, int] | None:
        """Get the move for the current player based on whether they are human or AI."""
        if player.strategy.is_human:
            return position  # For human players, the move should come from the UI
        else:
            return player.get_move(self.board)  # For AI players, get the move from their strategy
