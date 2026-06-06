"""Utility functions for the Streamlit app"""

import streamlit as st

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
    return st.session_state.start_new_game
