"""File of tests for the player class used in the Tic Tac Toe game."""

from config.test_settings import BOARD_SIZE_TEST
from core.player import Player
from core.board import Board
from core.strategies import HumanStrategy, RandomAIStrategy


class TestPlayer:
    """Test class for the Player dataclass."""

    def setup_method(self):
        """Initialize a test board before each execution."""
        self.board = Board(size=BOARD_SIZE_TEST)

    def test_player_initialization(self):
        """Test that the attributes of the dataclass are correctly initialized."""
        strategy = HumanStrategy()
        player = Player(name="Player", symbol="X", strategy=strategy)
        
        assert player.name == "Player"
        assert player.symbol == "X"
        assert player.strategy == strategy

    def test_player_get_move_human(self):
        """Test that get_move delegates correctly to HumanStrategy (returns None)."""
        player = Player(name="Player", symbol="X", strategy=HumanStrategy())
        
        result = player.get_move(self.board)
        assert result is None

    def test_player_get_move_ai(self):
        """Test that get_move delegates to RandomAIStrategy and returns a valid move."""
        player = Player(name="AI Player", symbol="O", strategy=RandomAIStrategy())
        
        # Create board state with only one free cell at (0, 0)
        self.board.set_board(
            [[None, "X", "O"],
             ["O", "X", "X"],
             ["X", "O", "O"]]
        )
        
        result = player.get_move(self.board)
        assert result == (0, 0)
