"""File containing the main functions to render the sidebar of the Streamlit app."""

import streamlit as st

from config.settings import SYMBOL_X, SYMBOL_O
from config.ui import BOARD_SYMBOLS, UI_MESSAGES


### SIDEBAR OPTIONS RENDERING ###
def render_side_options(game_in_progress: bool) -> None:
    """
    Render the game options for the user to select game options by registering in session state.

    Args:
        game_in_progress (bool): A boolean indicating whether a game is in progress.
    """

    with st.sidebar:
        st.sidebar.title(UI_MESSAGES["options_title"])

        st.subheader(UI_MESSAGES["symbol_options"])
        player_symbol = st.sidebar.selectbox(
            label=UI_MESSAGES["choose_symbol"],
            key="player_symbol",
            options=[BOARD_SYMBOLS[SYMBOL_X], BOARD_SYMBOLS[SYMBOL_O]],
            disabled=game_in_progress
        )
        st.text(UI_MESSAGES["symbol_info"].format(BOARD_SYMBOLS[SYMBOL_X]))

        st.divider()
        if st.button(
            label=UI_MESSAGES["launch"],
            key="launch_button",
            disabled=game_in_progress
        ):
            player_symbol = SYMBOL_X if player_symbol == BOARD_SYMBOLS[SYMBOL_X] else SYMBOL_O
            
            st.session_state.start_new_game = True
            st.session_state.options = {
                "player_symbol": player_symbol
            }
