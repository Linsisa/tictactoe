"""Utility functions for the Streamlit app"""

import streamlit as st

from time import sleep
from config.settings import BOARD_SIZE, WIN_LENGTH, SYMBOL_X, SYMBOL_O, AI_SLEEP_TIME
from config.ui import HUMAN_PLAYER_NAME, AI_PLAYER_NAME
from core.game_manager import GameManager
from core.player import Player
from core.strategies import HumanStrategy, RandomAIStrategy


def refresh_app_rendering() -> None:
    """Refresh the Streamlit app rendering to reflect changes in the game state."""
    st.rerun()


def is_game_in_progress() -> bool:
    """Return True if a game is currently in progress, False otherwise."""
    return game_exists() and not st.session_state.game.is_game_over()


def game_exists() -> bool:
    """Return True if a game exists in session state, False otherwise."""
    return st.session_state.game is not None


### Game creation and management functions ###
def create_game(human_symbol: str) -> None:
    """
    Initialize the game with 2 players (human and AI) based on the symbol chosen by the user

    Args:
        human_symbol (str): The symbol chosen by the user for the human player.
    """
    ai_symbol = SYMBOL_O if human_symbol == SYMBOL_X else SYMBOL_X

    # Create player instances
    player_1 = Player(HUMAN_PLAYER_NAME, human_symbol, HumanStrategy())
    player_2 = Player(AI_PLAYER_NAME,    ai_symbol,    RandomAIStrategy())

    # X always starts first, _define_starting_player handles this in GameManager
    st.session_state.game = GameManager(player_1, player_2, BOARD_SIZE, WIN_LENGTH)

def should_start_new_game() -> bool:
    """Return True if the conditions to start a new game are met, False otherwise."""
    return st.session_state.options is not None and not is_game_in_progress()


### Turn handling functions ###
def handle_turn(game: "GameManager", clicked_cell: tuple[int, int] | None) -> None:
    """
    Handle the current turn for both AI and human players based on the game state and user interactions.

    Args:
        game (GameManager): The current game manager instance containing the game state.
        clicked_cell (tuple[int, int] | None): The row and column indices of the cell clicked by the user, or None if no cell was clicked.
    """
    is_ai_turn = game.is_ai_input_allowed()
    
    if is_ai_turn:
        handle_ai_turn(game)
    elif clicked_cell:
        handle_human_turn(game, clicked_cell)
    else:
        return
    
    refresh_app_rendering()

def handle_ai_turn(game: "GameManager") -> None:
    """
    Make AI play if it's AI's turn and the game is not over, then refresh the app rendering.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    sleep(AI_SLEEP_TIME)  # Simulate thinking time for the AI
    game.play_turn()  # Make AI play its turn (position is None, AI will choose its move)

def handle_human_turn(game: "GameManager", clicked_cell: tuple[int, int]) -> None:
    """
    Handle the human player's turn by playing the move at the clicked cell and refreshing the app rendering.

    Args:        
        game (GameManager): The current game manager instance containing the game state.
        clicked_cell (tuple[int, int]): The row and column indices of the cell clicked by the user.
    """
    game.play_turn(position=clicked_cell)
