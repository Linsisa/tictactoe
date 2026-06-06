"""File of the UI components for the Tic Tac Toe game, including the main game window"""

import streamlit as st

from config.settings import SYMBOL_X, SYMBOL_O
from config.ui import BOARD_SYMBOLS, ICONS, UI_MESSAGES, GAME_RULES
from core.game_manager import GameManager


### RULES RENDERING ###
def render_rules() -> None:
    """
    Render the game rules in a expander on the main page of the application, allowing users to understand how to play the game and what the rules are.
    """
    with st.expander(UI_MESSAGES["rules_expander"]):
        st.text(GAME_RULES.format(BOARD_SYMBOLS[SYMBOL_X], BOARD_SYMBOLS[SYMBOL_O], BOARD_SYMBOLS[SYMBOL_X]))


### GAME OVER SECTION RENDERING ###
def render_game_over(game: GameManager) -> None:
    """
    Render the end game screen with the result of the game and the option to replay.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if game.is_winner():
        success_message = UI_MESSAGES["victory"].format(game.get_winner().name, game.get_winner().symbol)
        st.success(success_message, icon=ICONS["victory"])
    else:
        st.info(UI_MESSAGES["draw"], icon=ICONS["draw"])

    if st.button(UI_MESSAGES["quick_restart"]):
        game.reset_game()
        st.rerun()
