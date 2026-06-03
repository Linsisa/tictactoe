"""File of the GameManager class, which manages the overall game flow and state for the Tic Tac Toe game."""

from core.board import Board
from core.player import Player
from core.rules import check_winner, check_draw
from core.strategies import HumanStrategy
from config.settings import SYMBOL_X


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
        - If the current player is human, `move` should be provided by the UI.
        - If it's the AI, `move` can be None and will be chosen by the strategy.

        Args:
            position (tuple[int, int] | None): The row and column indices for the move, or None for AI.

        Returns:
            bool: True if the move was played, False otherwise.
        """
        # Stop if the game is over, no more moves can be played.
        if self.game_over:
            return False
        
        player = self.get_current_player()
        
        # Second step, get the move from the current player strategy. 
        # If it's a human player, the move should come from the UI,
        # so we use the `position` argument. 
        # If it's an AI player, we call the `get_move` method of the 
        # player's strategy to determine the move chosen by the AI.
        if isinstance(player.strategy, HumanStrategy):
            if position is None:
                return False
            move = position 
        else: # In this case, the player is an AI, so we get the move from the strategy.
            move = player.get_move(self.board)
        
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

        # Check wheter the last move created a winner.
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

    def get_current_player(self) -> Player:
        """Return the current player."""
        return self.players[self.current_player_index]

    def _switch_player(self) -> None:
        """Switch the current player to the other player."""
        self.current_player_index = 1 - self.current_player_index

    def _define_starting_player(self) -> int:
        """Select the player with the 'X' symbol as the starting player."""
        starting_player = 0 if self.players[0].symbol == SYMBOL_X else 1
        return starting_player