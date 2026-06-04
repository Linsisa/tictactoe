"""Test file for the board Class"""

from core.board import Board, EMPTY_CELL
from config.settings import BOARD_SIZE


class TestBoard:
    """Test class for the Board class."""
    
    # Define method executed before each test method
    def setup_method(self):
        """Set up a new board instance before each test."""
        self.board = Board(size=BOARD_SIZE)

    def test_board_initialization(self):
        """Test that the board created by the Board class is initialized correctly."""
        expected_board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        assert self.board.get_current_board() == expected_board

    def test_board_reset(self):
        """Test that the reset board method correctly resets the board to its initial state."""
        self.board.apply_move((0, 0), "X")
        self.board.apply_move((1, 1), "O")

        self.board.reset_board()

        expected_board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        assert self.board.get_current_board() == expected_board

    ### Apply move tests ###
    def test_apply_move_success(self):
        """Test that a valid move is applied correctly to the board."""
        result = self.board.apply_move((0, 0), "X")

        assert result is True
        assert self.board.get_current_board()[0][0] == "X"

    def test_apply_move_cell_already_occupied(self):
        """Test that a move to an occupied cell is not applied."""
        # Apply the first move
        self.board.apply_move((0, 0), "X")

        # Try to apply a move to the same position
        result = self.board.apply_move((0, 0), "O")

        assert result is False
        assert self.board.get_current_board()[0][0] == "X"

    def test_apply_move_same_player_same_cell(self):
        """Test that a move to the same cell by the same player is not applied."""
        # Apply the first move
        self.board.apply_move((0, 0), "X")

        # Try to apply a move to the same position by the same player
        result = self.board.apply_move((0, 0), "X")

        assert result is False
        assert self.board.get_current_board()[0][0] == "X"

    def test_apply_move_cell_out_of_bounds(self):
        """Test that a move to an out-of-bounds cell is not applied."""
        position_out_of_bounds_negative = (-1, -1)  # This position is out of bounds
        result_1 = self.board.apply_move(position_out_of_bounds_negative, "X")

        position_out_of_bounds_positive = (BOARD_SIZE, BOARD_SIZE)  # This position is out of bounds
        result_2 = self.board.apply_move(position_out_of_bounds_positive, "X")

        assert result_1 is False
        assert result_2 is False
    
    ### Get free cells tests ###
    def test_get_free_cells_initial(self):
        """Test that the get_free_cells method returns all cells when the board is empty."""
        expected_free_cells = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        
        assert set(self.board.get_free_cells()) == set(expected_free_cells)

    def test_get_free_cells(self):
        """Test that the get_free_cells method returns the correct list of free cells."""
        # Apply some moves to change the board state
        self.board.apply_move((0, 0), "X")
        self.board.apply_move((1, 1), "O")

        expected_free_cells = [
                    (0, 1), (0, 2),
            (1, 0),         (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]

        assert set(self.board.get_free_cells()) == set(expected_free_cells)

    def test_get_free_cells_full_board(self):
        """Test that the get_free_cells method returns an empty list when the board is full."""
        # Fill the board completely
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.board.apply_move((row, col), "X")

        assert self.board.get_free_cells() == []

    ### Is full tests ###
    def test_is_full_empty_board(self):
        """Test that the is_full method returns False for an empty board."""
        assert self.board.is_full() is False
    
    def test_is_full_partial_board(self):
        """Test that the is_full method returns False for a partially filled board."""
        self.board.apply_move((0, 0), "X")
        self.board.apply_move((1, 1), "O")

        assert self.board.is_full() is False
    
    def test_is_full_full_board(self):
        """Test that the is_full method returns True for a full board."""
        # Fill the board completely
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.board.apply_move((row, col), "X")

        assert self.board.is_full() is True

    ### Is position in bounds tests ###
    def test_is_position_in_bounds_valid(self):
        """Test that the is_position_in_bounds method returns True for valid positions."""
        assert self.board.is_position_in_bounds((0, 0)) is True
        assert self.board.is_position_in_bounds((1, 1)) is True
        assert self.board.is_position_in_bounds((2, 2)) is True

    def test_is_position_in_bounds_invalid(self):
        """Test that the is_position_in_bounds method returns False for invalid positions."""
        assert self.board.is_position_in_bounds((-1, 0)) is False
        assert self.board.is_position_in_bounds((0, -1)) is False
        assert self.board.is_position_in_bounds((BOARD_SIZE, 0)) is False
        assert self.board.is_position_in_bounds((0, BOARD_SIZE)) is False