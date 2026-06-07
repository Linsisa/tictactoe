"""File of the various UI components for the Tic Tac Toe game"""

import streamlit as st
import st_yled as sty

from app_utils import game_exists, is_game_in_progress, refresh_app_rendering
from config.settings import SYMBOL_X, SYMBOL_O
from config.ui import BOARD_SYMBOLS, ICONS, UI_MESSAGES, GAME_RULES
from core.game_manager import GameManager
from ui.board import render_board


### RULES RENDERING ###
def render_rules() -> None:
    """
    Render the game rules in a expander on the main page of the application, allowing users to understand how to play the game and what the rules are.
    """
    with st.expander(UI_MESSAGES["rules_expander"]):
        st.text(GAME_RULES.format(BOARD_SYMBOLS[SYMBOL_X], BOARD_SYMBOLS[SYMBOL_O], BOARD_SYMBOLS[SYMBOL_X]))


### CURRENT TURN RENDERING ###
def render_current_turn(game: GameManager) -> None:
    """
    Render the current turn information at the top of the game screen.
    
    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if not game.is_game_over():
        st.info(UI_MESSAGES["current_turn"] + f" **{game.get_current_player().name} ({game.get_current_player().symbol})**")


### GAME RENDERING ###
def render_game_status() -> None:
    """
    Render the current game status, (Selected options, game in progress, game over)
    """
    sty.init()
    if not game_exists():
        sty.text(UI_MESSAGES["choose_options"],
                font_size="1.25rem", 
                color="#6B7280"
                )
        return
    
    if is_game_in_progress():
        sty.text(UI_MESSAGES["game_in_progress"],
                font_size="1.25rem",
                color="#6B7280"
                )
        return
    
    sty.text(UI_MESSAGES["game_over"],
                font_size="1.25rem",
                color="#6B7280"
                )

def render_game() -> None:
    """
    Render the main game screen, including the current turn,
    the game board, and handle the game logic for both human and AI turns.
    Also handles the end game screen when the game is over.
    """
    if game_exists():
        # Get the current game manager instance from session state
        game = st.session_state.game

        # Display the current turn information at the top of the game screen
        render_current_turn(game)

        # Render the game board and get the position of the cell clicked by the user (if any)
        clicked_cell = render_board(game)
        
        if game.play_turn(clicked_cell):
            refresh_app_rendering()

        # Check if game is over to render the end game screen with the result and the option to replay
        if game.is_game_over():
            render_game_over(game)


### GAMEOVER SECTION RENDERING ###
def render_game_over(game: GameManager) -> None:
    """
    Render the end game screen with the result of the game and the option to replay.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if game.get_winner() is not None:
        success_message = UI_MESSAGES["victory"].format(game.get_winner().name, game.get_winner().symbol)
        st.success(success_message, icon=ICONS["victory"])
    else:
        st.info(UI_MESSAGES["draw"], icon=ICONS["draw"])

    if st.button(UI_MESSAGES["quick_restart"]):
        game.reset_game()
        refresh_app_rendering()
