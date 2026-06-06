"""Utility functions for the Streamlit app"""

import streamlit as st


def refresh_app_rendering() -> None:
    """Refresh the Streamlit app rendering to reflect changes in the game state."""
    st.rerun()


def is_game_in_progress() -> bool:
    """Return True if a game is currently in progress, False otherwise."""
    return game_exists() and not st.session_state.game.is_game_over()


def game_exists() -> bool:
    """Return True if a game exists in session state, False otherwise."""
    return st.session_state.game is not None
