"""File of the UI components for the Tic Tac Toe game, including the main game window"""

import streamlit as st

from config.ui import ICONS, UI_MESSAGES
from core.game_manager import GameManager


def render_board(game: GameManager) -> tuple[int, int] | None:
    """
    Render the game board using Streamlit.
    
    Args:
        game (GameManager): The current game manager instance containing the game state.
        
    Returns:
        tuple[int, int] | None: The position of the cell clicked by the user,
        or None if no cell was clicked.
    """

    # Get the current state of the board from the game manager and determine the size of the board
    board = game.get_current_board_state()
    row_num = len(board)
    col_num = len(board[0]) if board else 0

    is_human_turn = game.is_current_player_human()

    disable_buttons = (
        game.game_over 
        or not is_human_turn
    )

    # Render the board as a grid of buttons
    for row in range(row_num):
        cols = st.columns(col_num) 

        for col in range(col_num):
            cell_value = board[row][col]
            with cols[col]:
                if st.button(
                    label=cell_value if cell_value else " ",
                    key=f"cell_{row}_{col}",
                    width=40,
                    disabled=disable_buttons
                ):
                    return (row, col)

    return None


def render_game_over(game: GameManager) -> None:
    """
    Render the end game screen with the result of the game and the option to replay.

    Args:
        game (GameManager): The current game manager instance containing the game state.
    """
    if game.winner:
        success_message = UI_MESSAGES["victory"].format(game.winner.name, game.winner.symbol)
        st.success(success_message, icon=ICONS["victory"])
    else:
        st.info(UI_MESSAGES["draw"], icon=ICONS["draw"])

    if st.button(UI_MESSAGES["play_again"]):
        game.reset_game()
        st.rerun()
