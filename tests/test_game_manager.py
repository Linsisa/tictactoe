"""File of tests for the GameManager class."""

from config.settings import SYMBOL_X, SYMBOL_O
from config.test_settings import BOARD_SIZE_TEST, WIN_LENGTH_TEST
from core.board import Board
from core.game_manager import GameManager
from core.player import Player
from core.strategies import HumanStrategy, RandomAIStrategy


class TestGameManager:
    """Test class for GameManager."""

    def setup_method(self):
        """Initialize a GameManager instance before each test."""
        self.player1 = Player(name="Player 1", symbol=SYMBOL_X, strategy=HumanStrategy())
        self.player2 = Player(name="Player 2", symbol=SYMBOL_O, strategy=RandomAIStrategy())
        self.expected_empty_board = [[None for _ in range(BOARD_SIZE_TEST)] for _ in range(BOARD_SIZE_TEST)]

        self.game_manager = GameManager(self.player1, self.player2, BOARD_SIZE_TEST, WIN_LENGTH_TEST)

    def test_game_initialization(self):
        """Test that the GameManager initializes correctly."""
        assert self.game_manager.players == [self.player1, self.player2]
        assert isinstance(self.game_manager._board, Board)
        assert self.game_manager.get_current_board_state() == self.expected_empty_board
        assert self.game_manager._win_length == WIN_LENGTH_TEST
        assert self.game_manager.get_current_player_index() == 0
        assert self.game_manager.get_winner() is None
        assert self.game_manager.game_over is False
        assert self.game_manager.get_last_move() is None

    def test_player_with_symbol_X_starts_first(self):
        """Test that the player with symbol 'X' starts first."""
        current_player_index = self.game_manager.get_current_player_index()
        assert current_player_index == 0
        assert self.game_manager.players[current_player_index].symbol == SYMBOL_X

        # Create a new GameManager where the second player has symbol 'X' and check that it starts first
        game_manager_2 = GameManager(
            Player(name="Player 1", symbol=SYMBOL_O, strategy=HumanStrategy()),
            Player(name="Player 2", symbol=SYMBOL_X, strategy=RandomAIStrategy()),
            BOARD_SIZE_TEST,
            WIN_LENGTH_TEST
        )
        current_player_index = game_manager_2.get_current_player_index()
        assert current_player_index == 1
        assert game_manager_2.players[current_player_index].symbol == SYMBOL_X

    ### Test reset_game method ###
    def test_reset_game(self):
        """Test that reset_game correctly resets the game state."""
        # Simulate some game state changes
        self.game_manager.play_turn(position=(0, 0))  # Player 1 plays a move
        self.game_manager._set_winner(0)  # Set player 1 as the winner
        self.game_manager.game_over = True

        # Call reset_game and check that everything is reset to initial state
        self.game_manager.reset_game()
        
        assert self.game_manager.get_current_board_state() == self.expected_empty_board
        assert self.game_manager.get_current_player_index() == 0  # Player with 'X' should start first
        assert self.game_manager.get_winner() is None
        assert self.game_manager.game_over is False
        assert self.game_manager.get_last_move() is None
        assert self.game_manager._win_length == WIN_LENGTH_TEST  # win_length should remain unchanged

    ### Tests for player-related methods ###
    def test_switch_player(self):
        """Test that _switch_player correctly switches between players."""
        initial_player_index = self.game_manager.get_current_player_index()
        
        # Switch player and check that the index has changed
        self.game_manager._switch_player()
        assert self.game_manager.get_current_player_index() == 1 - initial_player_index
        
        # Switch back and check again
        self.game_manager._switch_player()
        assert self.game_manager.get_current_player_index() == initial_player_index

    def test_define_first_player(self):
        """Test that _define_starting_player correctly identifies the starting player based on symbol."""
        # Player 1 has symbol 'X', so they should start first
        assert self.game_manager._define_starting_player() == 0

        # Create a new GameManager where player 2 has symbol 'X' and check that they start first
        game_manager_2 = GameManager(
            Player(name="Player 1", symbol=SYMBOL_O, strategy=HumanStrategy()),
            Player(name="Player 2", symbol=SYMBOL_X, strategy=RandomAIStrategy()),
            BOARD_SIZE_TEST,
            WIN_LENGTH_TEST
        )
        assert game_manager_2._define_starting_player() == 1

    ### Tests for play_turn method ###
        ## Human player turn ##
    def test_play_turn_human_valid_move(self):
        """Test that play_turn correctly processes a valid move."""
        # Player 1 is a human player, so we provide a valid move position
        valid_move_position = (0, 0)
        result = self.game_manager.play_turn(position=valid_move_position)
        
        assert result is True
        assert self.game_manager.get_board_cell(0, 0) == SYMBOL_X
        assert self.game_manager.get_last_move() == valid_move_position
        assert self.game_manager.get_current_player_index() == 1  # Player should have switched after a successful turn
    
    def test_play_turn_human_empty_move(self):
        """Test that play_turn correctly handles an move equal to None."""
        empty_move_position = None
        result = self.game_manager.play_turn(position=empty_move_position)
        
        assert result is False
        assert self.game_manager.get_last_move() is None  # last_move should not be updated after an invalid turn
        assert self.game_manager.get_current_player_index() == 0  # Player should not have switched after an invalid turn

    def test_play_turn_human_invalid_move(self):
        """Test that play_turn correctly handles an invalid move (already occupied cell)."""
        self.game_manager.play_turn(position=(0, 0))  # Player 1 places 'X' at (0, 0)
        self.game_manager.play_turn()  # Player 2 (AI) plays a turn, but we don't care where it moves for this test
        last_AI_move = self.game_manager.get_last_move()
        assert last_AI_move is not None  # Ensure the AI made a move

        occupied_position = (0, 0)  # This cell is already occupied.
        result = self.game_manager.play_turn(position=occupied_position)
        
        assert result is False
        assert self.game_manager.get_last_move() == last_AI_move  # last_move should not be updated after an invalid turn
        assert self.game_manager.get_current_player_index() == 0  # Player should not have switched after an invalid turn

        ## AI player turn ##
    def test_play_turn_ai_move(self):
        """Test that play_turn correctly processes a turn for an AI player."""
        self.game_manager.play_turn(position=(0, 0))  # Player 1 (human)

        result = self.game_manager.play_turn()  # Player 2 (AI) plays a turn (move determined by strategy)
        last_move = self.game_manager.get_last_move()

        assert result is True
        assert self.game_manager.get_last_move() is not None

        assert self.game_manager.get_board_cell(last_move[0], last_move[1]) == SYMBOL_O
        assert self.game_manager.get_current_player_index() == 0  # Player should have switched back to player 1 after AI's turn

        ## Test applying a move after game is over ##
    def test_play_turn_after_game_over(self):
        """Test that play_turn does not allow moves after the game is over."""
        # Simulate a game over state
        self.game_manager.game_over = True

        result = self.game_manager.play_turn(position=(0, 0)) # Player 1 tries to play a move after game is over
        
        assert result is False
        assert self.game_manager.get_board_cell(0, 0) is None  # Move should not be applied to the board
        assert self.game_manager.get_current_player_index() == 0  # Player should not have switched after an invalid turn

    ### Tests for _after_turn method ###
    def test_after_turn_winner(self):
        """Test that _after_turn correctly identifies a winner and ends the game."""
        # Simulate a winning move for player 1
        self.game_manager._set_board(
            [[SYMBOL_X, SYMBOL_X, SYMBOL_X],
             [SYMBOL_O, SYMBOL_O, None],
             [None,     None,     None]]
        )
        self.game_manager._set_last_move((0, 2))  # Player 1 places 'X' at (0, 2) to win

        self.game_manager._after_turn()
        
        assert self.game_manager.get_winner() == self.player1
        assert self.game_manager.game_over is True

    def test_after_turn_draw(self):
        """Test that _after_turn correctly identifies a draw and ends the game."""
        # Simulate a draw state
        self.game_manager._set_board(
            [[SYMBOL_X, SYMBOL_O, SYMBOL_X],
             [SYMBOL_O, SYMBOL_X, SYMBOL_O],
             [SYMBOL_O, SYMBOL_X, SYMBOL_O]]
        )
        self.game_manager._set_last_move((1, 1))  # Last move was at (1, 1)

        self.game_manager._after_turn()
        
        assert self.game_manager.get_winner() is None
        assert self.game_manager.game_over is True
