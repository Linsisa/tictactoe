"""File of the UI components for the Tic Tac Toe game, including the main game window"""

import streamlit as st

from config.ui import ICONS, UI_MESSAGES, BOARD_SYMBOLS
from config.settings import SYMBOL_X, SYMBOL_O
from core.game_manager import GameManager


### SIDEBAR OPTIONS RENDERING
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
            st.session_state.options = {
                "player_symbol": player_symbol
            }


### BOARD RENDERING
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
    disable_buttons = game.game_over or not is_human_turn


    padding = max(1, 8 - col_num)  # Adjust padding based on the number of columns
    col_gauche, col_centre, col_droite = st.columns([padding, col_num, padding])

    clicked_cell = None

    st.html("<div class='tictactoe-board'>")  # Add a wrapper div with a specific class for styling
    with col_centre:
        # Render the board as a grid of buttons
        for row in range(row_num):
            cols = st.columns(col_num) 

            for col in range(col_num):
                cell_value = BOARD_SYMBOLS.get(board[row][col])  # Display the UI symbol based on the board value
                
                with cols[col]:
                    if st.button(
                        label=cell_value if cell_value else " ",
                        key=f"cell_{row}_{col}",
                        disabled=disable_buttons,
                        use_container_width=True
                    ):
                        clicked_cell = (row, col)
    st.html("</div>") 

    return clicked_cell


## GAME OVER SECTION RENDERING
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

    if st.button(UI_MESSAGES["quick_restart"]):
        game.reset_game()
        st.rerun()
