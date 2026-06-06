"""Utility functions for the Streamlit app"""

import streamlit as st

from time import sleep
from config.settings import AI_SLEEP_TIME


def refresh_app_rendering() -> None:
    """Refresh the Streamlit app rendering to reflect changes in the game state."""
    st.rerun()


def is_game_in_progress() -> bool:
    """Return True if a game is currently in progress, False otherwise."""
    return game_exists() and not st.session_state.game.is_game_over()


def game_exists() -> bool:
    """Return True if a game exists in session state, False otherwise."""
    return st.session_state.game is not None


### Turn handling functions ###
def handle_turn(game: "GameManager", clicked_cell: tuple[int, int] | None) -> None:
    """
    Handle the current turn for both AI and human players based on the game state and user interactions.

    Args:
        game (GameManager): The current game manager instance containing the game state.
        clicked_cell (tuple[int, int] | None): The row and column indices of the cell clicked by the user, or None if no cell was clicked.
    """
    is_ai_turn = game.is_ai_input_allowed()
    turn_handled = False
    
    if is_ai_turn:
        handle_ai_turn(game)
        turn_handled = True
    elif clicked_cell:
        handle_human_turn(game, clicked_cell)
        turn_handled = True

    if turn_handled:
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
